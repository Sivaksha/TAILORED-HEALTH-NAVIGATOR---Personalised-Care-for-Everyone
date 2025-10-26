# 🩺 Tailored Health Navigator – Personalized Care for Everyone

An **AI-powered health management system** that provides personalized healthcare support, combining **disease prediction, medication tracking, secure document storage, and interactive health dashboards** — all in one application.

Developed using **Python**, **Streamlit**, and **Flask**, the system integrates **Groq’s Large Language Model (LLM)** for symptom-based disease prediction and leverages **Twilio** and **PyWhatKit** for smart medication reminders.

---

## 🚀 Features

### 🧠 AI-Powered Disease Prediction
- Uses **Groq’s LLM (mistral-saba-24b)** through **LangChain** to analyze user symptoms.  
- Provides detailed health insights including:  
  - Disease description  
  - Prevention methods  
  - Diet recommendations  
  - Exercise suggestions  

### 💊 Smart Medication Reminder
- Sends medication alerts via:
  - **SMS (Twilio API)**
  - **WhatsApp (PyWhatKit)**
- Supports daily reminder scheduling.

### 📂 Secure Document Storage
- Upload and manage prescriptions, reports, and medical images.  
- Role-based access ensures only authorized users can view or delete files.  
- File uploads are sanitized and timestamped for security.

### 📊 Personalized Health Dashboard
- Log symptoms and medications over time.  
- Visualize data using **Plotly** interactive charts.  
- Track progress and analyze health trends.

### 🔐 User Authentication
- Registration and login system using **SQLite**.  
- Session state management for secure access.  
- Role-based personalization per user.

---
```text
## 🧩 System Architecture
 
User Interface
   │
   ├── Symptom Input → Disease Prediction (Groq LLM)
   ├── Medication Tracker → Reminder Service (Twilio / PyWhatKit)
   ├── Document Upload → Secure Storage (SQLite)
   └── Dashboard → Health Logs & Visualization (Plotly)
``` 
🧪 Example Use Case
- Register and log in to your account.
- Enter symptoms like "fever, cough" → AI predicts possible diseases.
- Set a medication reminder via SMS or WhatsApp.
- Upload prescriptions for future reference.
- Track your health trends through the dashboard.

🔒 Security and Ethics
- All data stored securely in SQLite with per-user access.
- Sensitive credentials stored as environment variables.
- AI acts as an assistant — not a substitute for medical diagnosis.
- Adheres to GDPR and HIPAA-aligned principles for prototype usage.

🚧 Future Enhancements
- Cloud deployment (AWS / Streamlit Cloud)
- Voice input & chatbot with memory
- Wearable device integration
- Multilingual support
- Multi-factor authentication & password hashing
- Doctor teleconsultation integration

📚 References

Based on research from IEEE, ACM, and Springer publications on AI in healthcare, IoT integration, and digital health systems.
