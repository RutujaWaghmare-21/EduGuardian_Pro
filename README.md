# EduGuardian Pro 🛡️

**AI-Driven Institutional Intelligence for Student Retention**

EduGuardian Pro is an end-to-end AI solution designed to solve the "Diagnostic Bottleneck" in education. By moving beyond simple grade tracking, it utilizes XGBoost-powered feature intersection to identify students at risk due to hidden socioeconomic barriers—such as commute poverty, digital gaps, and financial instability.

## 📂 Project Structure

```
EduGuardian_Pro/
├── static/
│   ├── index.html       # Student-facing 'Pulse' Interface (Data Ingestion)
│   └── dashboard.html   # Admin/Principal 'Intelligence' Dashboard (Visualization)
├── app.py               # FastAPI Backend (Intersectionality Logic & API)
├── model_engine.py      # AI Core (Random Forest/XGBoost & XAI Narratives)
├── requirements.txt     # Python Dependencies
├── schema.sql           # DPDP-Compliant Anonymized Database Schema
└── README.md            # Project Documentation
```

## 🚀 Key Features
1. **Behavioral Pulse Engine**  
Instead of static annual surveys, the system captures a real-time "Pulse" of student wellness, travel barriers, and academic confidence.

2. **Socio-Academic Feature Intersection**  
The AI doesn't just look at marks. It correlates data (e.g., Long Commute + Low Income) to identify high-risk students who might otherwise be invisible.

3. **Explainable AI (XAI) Narratives**  
No "black boxes." Every risk flag is accompanied by a human-readable story explaining the "Why," allowing mentors to provide empathetic, targeted support.

4. **Institutional Risk Heatmaps**  
Aggregates individual data into district-level intelligence, enabling policy-makers to allocate budgets (e.g., bicycle grants or data packs) where they are needed most.

## 🛠️ Technical Stack
- **Backend:** FastAPI (High-performance Python framework)
- **Machine Learning:** Scikit-Learn (XGBoost/RandomForest Ensemble)
- **Data Handling:** Pandas & NumPy
- **Frontend:** HTML5, CSS3 (Tailwind CSS), and Chart.js for live data visualization
- **Privacy:** DPDP-aligned data anonymization protocols

## ⚙️ Installation & Setup
### Clone the Repository  
git clone https://github.com/YOUR_USERNAME/EduGuardian_Pro_v2.git  
cdd EduGuardian_Pro 
### Install Dependencies  
pip install -r requirements.txt  
### Launch the Application  
python app.py  
### Access the Interface  
- Student Pulse: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Admin Dashboard: [http://127.0.0.1:8000/static/dashboard.html](http://127.0.0.1:8000/static/dashboard.html)

## 🛡️ Ethical AI & Privacy
- **Fairness:** The model is trained on socioeconomic barriers rather than sensitive demographic traits (gender/religion) to mitigate bias.
- **Inclusivity:** Optimized for low-bandwidth environments to support rural education.
- **Compliance:** All data is processed using UUIDs to ensure student anonymity under 2026 data protection standards.
