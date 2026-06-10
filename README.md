# EduGuardian Pro 🛡️

**AI-Driven Institutional Intelligence for Student Retention**

EduGuardian Pro is an end-to-end AI solution designed to solve the "Diagnostic Bottleneck" in education. By moving beyond simple grade tracking, it utilizes XGBoost-powered feature intersection to identify students at risk due to hidden socioeconomic barriers—such as commute poverty, digital gaps, and financial instability.

## 📂 Project Structure

```
EduGuardian_Pro/
├── static/
│   ├── index.html       # Student 'Pulse' Ingestion View
│   └── dashboard.html   # Admin 'Intelligence' Console
├── app.py               # Main FastAPI Application Engine (ML Inference & API Routing)
├── eduguardian_rf.joblib # Trained Random Forest Model Weights
├── scaler.joblib        # Scikit-learn Feature Scaling File
├── eduguardian.db       # Persistent SQLite Database Storage (Auto-generated)
├── .env                 # Local Environment Keys (Groq Cloud Storage)
└── requirements.txt     # Python Architecture Dependencies
```

## 🚀 Key Features
1. **Behavioral Pulse Engine**  
Instead of static annual surveys, the system captures a real-time "Pulse" of student wellness, travel barriers, and academic confidence.

2. **Socio-Academic Feature Intersection**  
The AI doesn't just look at marks. It correlates data (e.g., Long Commute + Low Income) to identify high-risk students who might otherwise be invisible.

3. **Explainable AI (XAI) Micro-Narratives**  
Replaces corporate "black-box" guessing by isolating exact profile anomalies using local feature extraction weights.

4. **Groq Cloud Llama-3.1 Pipeline:**  
Eliminates counselor writing fatigue by utilizing serverless inference to instantly write customized outreach text.

## 🛠️ Technical Stack
- **Backend:** FastAPI (High-performance Python framework)
- **Machine Learning:** Scikit-Learn (Ensembled Random Forest Engine)
- **Generative AI Layer:** Groq SDK Ecosystem (Llama-3.1-8b Inference Pipeline)
- **Data Handling:** Pandas & NumPy
- **Frontend:** HTML5, CSS3 (Tailwind CSS), and Chart.js for live data visualization
- **Privacy:** DPDP-aligned data anonymization protocols

## ⚙️ Installation & Setup
### Clone the Repository  
git clone https://github.com/RutujaWaghmare-21/EduGuardian_Pro  
cdd EduGuardian_Pro 
### Environment Configuration

Create a `.env` file in the root directory and add your cloud API credentials:

```plaintext
GROQ_API_KEY=your_groq_api_key_here
```
### Install Dependencies  
pip install -r requirements.txt  
### Launch the Application  
python app.py  
### Access the Interface  
- Student Data Ingest Hub: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Admin Dashboard: [http://127.0.0.1:8000/static/dashboard.html](http://127.0.0.1:8000/static/dashboard.html)

## 🛡️ Ethical AI & Privacy
- **Fairness:** The model is trained on socioeconomic barriers rather than sensitive demographic traits (gender/religion) to mitigate bias.
- **Inclusivity:** Optimized for low-bandwidth environments to support rural education.
- **Compliance:** All data is processed using UUIDs to ensure student anonymity under 2026 data protection standards.
