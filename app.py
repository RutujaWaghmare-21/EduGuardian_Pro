from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from model_engine import EduGuardianModel
import uvicorn

app = FastAPI(title="EduGuardian Pro v2 - Advanced Edition")
ai = EduGuardianModel()

# --- GLOBAL MEMORY FOR DYNAMIC DASHBOARD ---
all_assessments = []

class StudentInput(BaseModel):
    attendance: float
    marks: float
    wellness: float
    digital: int
    travel: float
    income: int
    scholarship: int

def match_resources(level, data):
    resources = []
    if level == "CRITICAL":
        resources.append("Immediate 1-on-1 Mentorship")
        resources.append("Emergency Financial Grant")
    if data.travel > 18:
        resources.append("Safe-Transport Stipend / Bicycle Grant")
    if data.wellness < 2.5:
        resources.append("Peer Support Group Referral")
    if data.digital == 0:
        resources.append("Digital Device Lending Program")
    if not resources:
        resources.append("Merit Excellence Program")
    return resources

def generate_narrative(data, analysis):
    narrative = f"The risk engine identifies {analysis['top_driver']} as the primary systemic barrier. "
    if data.travel > 15 and data.income == 1:
        narrative += "Structural travel barriers combined with economic vulnerability detected. "
    if analysis['probability'] > 0.7:
        narrative += "Immediate empathetic intervention is required. "
    else:
        narrative += "Current stability is high; maintain routine monitoring."
    return narrative

@app.post("/analyze_pro")
async def analyze_student(data: StudentInput):
    input_list = [data.attendance, data.marks, data.wellness, data.digital, data.travel, data.income, data.scholarship]
    prediction = ai.predict_pro(input_list)
    
    # STORE RESULT FOR DASHBOARD
    all_assessments.append({
        "probability": prediction["probability"],
        "level": prediction["level"],
        "driver": prediction["top_driver"]
    })
    
    counselor_msg = "Your journey matters. "
    if data.travel > 15 and data.income == 1:
        counselor_msg += "Your long commute is a burden given financial constraints. Let's look into transport grants."
    elif data.wellness < 3.0:
        counselor_msg += "Your wellness score is dipping. It's okay to reach out for support."
    else:
        counselor_msg += "You are on a steady path. Stay consistent!"

    return {
        "analysis": prediction,
        "recommendations": match_resources(prediction["level"], data),
        "human_story": generate_narrative(data, prediction),
        "counselor_voice": counselor_msg
    }
@app.get("/get_stats")
async def get_stats():
    total = len(all_assessments)
    if total == 0:
        return {"total": 0, "risk_counts": [0, 0, 0], "recent_probs": []}
    
    critical = len([x for x in all_assessments if x['level'] == 'CRITICAL'])
    elevated = len([x for x in all_assessments if x['level'] == 'ELEVATED'])
    stable = len([x for x in all_assessments if x['level'] == 'STABLE'])
    
    return {
        "total": total,
        "risk_counts": [critical, elevated, stable],
        "recent_probs": [x['probability'] for x in all_assessments[-10:]] 
    }

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def pulse_input(): return FileResponse('static/index.html')

@app.get("/admin")
async def admin_dashboard(): return FileResponse('static/dashboard.html')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)