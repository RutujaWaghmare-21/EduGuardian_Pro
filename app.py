
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional
import sqlite3, uuid, numpy as np, joblib, os, hashlib, hmac, base64, json, time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="EduGuardian Pro", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_FILE   = "eduguardian.db"
SECRET    = os.getenv("SECRET_KEY", "eduguardian-secret-2024")
MODEL_PATH, SCALER_PATH = "eduguardian_rf.joblib", "scaler.joblib"

# ── ML ──────────────────────────────────────────────────────────────────────
try:
    model  = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    REAL   = True
    print("✅  ML model loaded")
except Exception as e:
    REAL = False
    print(f"⚠️  Model missing ({e}) — fallback mode")

# ── AI CLIENT ───────────────────────────────────────────────────────────────
ai = OpenAI(base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY", ""))

# ── DATABASE ─────────────────────────────────────────────────────────────────
def init_db():
    with sqlite3.connect(DB_FILE) as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY, name TEXT, email TEXT UNIQUE,
            password_hash TEXT, role TEXT DEFAULT 'counselor',
            institution TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            last_login TEXT, total_analyses INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY, user_id TEXT,
            student_label TEXT DEFAULT 'Anonymous',
            attendance REAL, marks REAL, wellness REAL,
            digital INTEGER, travel REAL, income INTEGER, scholarship INTEGER,
            probability REAL, risk_level TEXT, primary_driver TEXT,
            confidence REAL, counselor_msg TEXT,
            recommendations TEXT, actionable_impact TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS students_anonymized (
            student_uuid TEXT PRIMARY KEY,
            probability REAL, risk_level TEXT, primary_driver TEXT
        );
        CREATE TABLE IF NOT EXISTS feedback (
            id TEXT PRIMARY KEY, user_id TEXT,
            message TEXT, created_at TEXT DEFAULT (datetime('now'))
        );
        """)
init_db()

# ── AUTH HELPERS ─────────────────────────────────────────────────────────────
def hash_pw(pw):
    return hashlib.sha256(f"{SECRET}{pw}".encode()).hexdigest()

def make_token(uid, email):
    payload = base64.b64encode(
        json.dumps({"id": uid, "email": email, "exp": time.time() + 86400*7}).encode()
    ).decode()
    sig = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"

def verify_token(token):
    try:
        payload, sig = token.split(".")
        if not hmac.compare_digest(
            sig, hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
        ): return None
        data = json.loads(base64.b64decode(payload).decode())
        return data if data["exp"] > time.time() else None
    except:
        return None

security = HTTPBearer(auto_error=False)

def get_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not creds: return None
    p = verify_token(creds.credentials)
    if not p: return None
    with sqlite3.connect(DB_FILE) as c:
        c.row_factory = sqlite3.Row
        u = c.execute("SELECT * FROM users WHERE id=?", (p["id"],)).fetchone()
    return dict(u) if u else None

def require_user(u=Depends(get_user)):
    if not u: raise HTTPException(401, "Authentication required")
    return u

# ── SCHEMAS ──────────────────────────────────────────────────────────────────
class Register(BaseModel):
    name: str; email: str; password: str
    institution: str = ""; role: str = "counselor"

class Login(BaseModel):
    email: str; password: str

class StudentInput(BaseModel):
    attendance:  float = Field(..., ge=0, le=100)
    marks:       float = Field(..., ge=0, le=100)
    wellness:    float = Field(..., ge=1, le=5)
    digital:     int   = Field(..., ge=0, le=1)
    travel:      float = Field(..., ge=0)
    income:      int   = Field(..., ge=1, le=3)
    scholarship: int   = Field(0,   ge=0, le=1)
    student_label: str = "Anonymous"

class Feedback(BaseModel):
    message: str

# ── FEATURE NAMES ─────────────────────────────────────────────────────────────
FEATURES = [
    'Attendance Rate (%)', 'Weekly Assessment Marks',
    'Emotional Wellness Score', 'Digital Access',
    'Travel Distance', 'Family Income Bracket', 'Scholarship Status'
]

def risk_weights(d: StudentInput):
    return [
        max(0, (95  - d.attendance) / 100),
        max(0, (75  - d.marks)      / 100),
        max(0, (4.0 - d.wellness)   / 5),
        0.25 if d.digital == 0 else 0,
        max(0, (d.travel - 15)      / 50),
        0.30 if d.income == 1 else (0.10 if d.income == 2 else 0),
        0.15 if d.scholarship == 0 else 0,
    ]

def get_resources(level, d, driver):
    res = []
    if level == "CRITICAL":
        res += ["Immediate 1-on-1 Mentorship", "Emergency Financial Grant"]
    if d.attendance < 75 or driver == FEATURES[0]:
        res.append("Automated Attendance Check-in Protocol")
    if d.marks < 50 or driver == FEATURES[1]:
        res.append("Peer Tutoring & Academic Support")
    elif d.marks >= 90 and level == "STABLE":
        res.append("Honors Academic Research Track")
    if d.travel > 18 or driver == FEATURES[4]:
        res.append("Safe-Transport Stipend / Bicycle Grant")
    if d.travel > 50:
        res.append("Remote-Learning Hybrid Schedule")
    if d.wellness < 2.5 or driver == FEATURES[2]:
        res.append("Professional Counseling Referral")
    elif d.wellness <= 3.5:
        res.append("Peer Counselor Mentorship Group")
    if d.digital == 0:
        res.append("Digital Device Lending & Wi-Fi Hotspot")
    if d.scholarship == 0 and d.income == 1:
        res.append("Scholarship Application Assistance")
    if not res:
        res.append("Standard Merit Excellence Tracks")
    return res

# ── AUTH ENDPOINTS ────────────────────────────────────────────────────────────
@app.post("/auth/register")
async def register(b: Register):
    uid = str(uuid.uuid4())
    try:
        with sqlite3.connect(DB_FILE) as c:
            c.execute("INSERT INTO users(id,name,email,password_hash,institution,role) VALUES(?,?,?,?,?,?)",
                      (uid, b.name, b.email, hash_pw(b.password), b.institution, b.role))
    except sqlite3.IntegrityError:
        raise HTTPException(400, "Email already registered")
    token = make_token(uid, b.email)
    return {"token": token, "user": {"id": uid, "name": b.name, "email": b.email,
                                      "role": b.role, "institution": b.institution}}

@app.post("/auth/login")
async def login(b: Login):
    with sqlite3.connect(DB_FILE) as c:
        c.row_factory = sqlite3.Row
        u = c.execute("SELECT * FROM users WHERE email=? AND password_hash=?",
                      (b.email, hash_pw(b.password))).fetchone()
    if not u: raise HTTPException(401, "Invalid credentials")
    u = dict(u)
    with sqlite3.connect(DB_FILE) as c:
        c.execute("UPDATE users SET last_login=datetime('now') WHERE id=?", (u["id"],))
    return {"token": make_token(u["id"], u["email"]),
            "user": {"id": u["id"], "name": u["name"], "email": u["email"],
                     "role": u["role"], "institution": u["institution"]}}

@app.get("/auth/me")
async def me(u=Depends(require_user)):
    return {k: u[k] for k in ["id","name","email","role","institution","total_analyses","created_at"]}

# ── CORE ANALYSIS ─────────────────────────────────────────────────────────────
@app.post("/analyze_pro")
async def analyze(data: StudentInput, user=Depends(get_user)):
    feats = [data.attendance, data.marks, data.wellness, data.digital,
             data.travel, data.income, data.scholarship]

    if REAL:
        scaled     = scaler.transform([feats])
        prob       = float(model.predict_proba(scaled)[0][1])
        tree_preds = [t.predict_proba(scaled)[0][1] for t in model.estimators_]
        confidence = round(max(0, 1 - np.std(tree_preds) * 2), 2)
        w          = risk_weights(data)
        driver     = FEATURES[int(np.argmax(w))] if max(w) > 0 else "No Active Stressors"
    else:
        # Deterministic fallback based on inputs
        w          = risk_weights(data)
        prob       = min(0.98, max(0.02, sum(w) / 3))
        confidence = 0.70
        driver     = FEATURES[int(np.argmax(w))] if max(w) > 0 else "No Active Stressors"

    level    = "CRITICAL" if prob > 0.70 else "ELEVATED" if prob > 0.40 else "STABLE"
    timeline = [round(max(0, prob * (0.85 ** i)), 3) for i in range(6)]
    recs     = get_resources(level, data, driver)
    red_pct  = 42 if level == "CRITICAL" else 25 if level == "ELEVATED" else 10
    impact   = f"{recs[0]} → {red_pct}% Risk Reduction"

    # AI counselor message
    try:
        ctx = (f"You are EduGuardian's empathetic AI mentor. "
               f"Write exactly 2 warm, direct sentences to support this student. "
               f"Risk: {level} ({prob*100:.1f}%). Primary concern: {driver}. "
               f"Attendance {data.attendance}%, Marks {data.marks}/100, "
               f"Wellness {data.wellness}/5, Travel {data.travel}km. "
               f"Speak directly to the student. Do NOT mention percentages or model scores.")
        r = ai.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "Warm academic advisor. 2 sentences only. No bullet points."},
                      {"role": "user", "content": ctx}],
            temperature=0.72, max_tokens=110
        )
        msg = r.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq error: {e}")
        msg = (f"Your journey matters deeply to us, and we see the challenges you're navigating. "
               f"Let's work together on '{driver}' — a focused intervention here can change your trajectory significantly.")

    # Persist
    aid     = str(uuid.uuid4())
    uid     = user["id"] if user else None
    with sqlite3.connect(DB_FILE) as c:
        c.execute("""INSERT INTO analyses(id,user_id,student_label,attendance,marks,wellness,
                     digital,travel,income,scholarship,probability,risk_level,primary_driver,
                     confidence,counselor_msg,recommendations,actionable_impact)
                     VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (aid, uid, data.student_label, data.attendance, data.marks, data.wellness,
                   data.digital, data.travel, data.income, data.scholarship,
                   prob, level, driver, confidence, msg, json.dumps(recs), impact))
        c.execute("INSERT OR IGNORE INTO students_anonymized VALUES(?,?,?,?)",
                  (aid, prob, level, driver))
        if uid:
            c.execute("UPDATE users SET total_analyses=total_analyses+1 WHERE id=?", (uid,))

    return {
        "id": aid,
        "analysis": {
            "probability": prob, "confidence": confidence,
            "level": level, "timeline": timeline, "top_driver": driver
        },
        "recommendations": recs,
        "human_story": f"The AI engine isolated '{driver}' as the dominant systemic factor.",
        "counselor_voice": msg,
        "actionable_impact": impact
    }

# ── HISTORY ───────────────────────────────────────────────────────────────────
@app.get("/history")
async def history(u=Depends(require_user)):
    with sqlite3.connect(DB_FILE) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("SELECT * FROM analyses WHERE user_id=? ORDER BY created_at DESC LIMIT 50",
                         (u["id"],)).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["recommendations"] = json.loads(d.get("recommendations") or "[]")
        out.append(d)
    return out

# ── STATS (legacy) ────────────────────────────────────────────────────────────
@app.get("/get_stats")
async def get_stats():
    with sqlite3.connect(DB_FILE) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("SELECT * FROM students_anonymized").fetchall()
    total = len(rows)
    if not total:
        return {"total": 0, "risk_counts": [0,0,0], "recent_probs": []}
    return {
        "total": total,
        "risk_counts": [
            sum(1 for r in rows if r["risk_level"] == "CRITICAL"),
            sum(1 for r in rows if r["risk_level"] == "ELEVATED"),
            sum(1 for r in rows if r["risk_level"] == "STABLE"),
        ],
        "recent_probs": [r["probability"] for r in rows[-10:]]
    }

# ── ADMIN STATS (extended) ────────────────────────────────────────────────────
@app.get("/admin_stats")
async def admin_stats(user=Depends(get_user)):
    with sqlite3.connect(DB_FILE) as c:
        c.row_factory = sqlite3.Row
        all_a  = c.execute("SELECT * FROM analyses ORDER BY created_at DESC").fetchall()
        u_count = c.execute("SELECT COUNT(*) as n FROM users").fetchone()["n"]

    total = len(all_a)
    if not total:
        return {"total": 0, "users_count": u_count, "risk_counts": [0,0,0],
                "recent_probs": [], "recent_cases": [], "driver_counts": {}}

    # Driver frequency map
    driver_counts = {}
    for r in all_a:
        d = r["primary_driver"] or "Unknown"
        driver_counts[d] = driver_counts.get(d, 0) + 1

    recent = []
    for r in all_a[:20]:
        recent.append({
            "id": r["id"][:8],
            "label": r["student_label"],
            "risk_level": r["risk_level"],
            "probability": r["probability"],
            "confidence": r["confidence"],
            "primary_driver": r["primary_driver"],
            "created_at": r["created_at"]
        })

    return {
        "total": total,
        "users_count": u_count,
        "risk_counts": [
            sum(1 for r in all_a if r["risk_level"] == "CRITICAL"),
            sum(1 for r in all_a if r["risk_level"] == "ELEVATED"),
            sum(1 for r in all_a if r["risk_level"] == "STABLE"),
        ],
        "recent_probs":  [r["probability"] for r in all_a[-10:]],
        "recent_cases":  recent,
        "driver_counts": driver_counts
    }

# ── FEEDBACK ──────────────────────────────────────────────────────────────────
@app.post("/feedback")
async def feedback(b: Feedback, user=Depends(get_user)):
    with sqlite3.connect(DB_FILE) as c:
        c.execute("INSERT INTO feedback(id,user_id,message) VALUES(?,?,?)",
                  (str(uuid.uuid4()), user["id"] if user else None, b.message))
    return {"status": "received"}

# ── HEALTH CHECK ──────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": REAL, "version": "2.0.0"}

# ── STATIC ────────────────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.get("/admin")
async def admin():
    return FileResponse("static/dashboard.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
