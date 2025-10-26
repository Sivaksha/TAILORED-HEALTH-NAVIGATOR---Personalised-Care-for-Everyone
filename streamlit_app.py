#streamlit_app.py

import streamlit as st
import sqlite3
import os
import schedule
import time
from twilio.rest import Client
from datetime import datetime
import threading

# Initialize database
DATABASE = "documents.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Symptom-based disease data
disease_data = {
    "fever": {
        "disease": "Common Cold",
        "description": "A viral infection causing sneezing, runny nose, and fever.",
        "prevention": "Wash hands regularly, avoid close contact with infected people.",
        "diet": "Drink warm fluids, eat fruits rich in Vitamin C.",
        "exercise": "Light stretching or walking if possible."
    },
    "cough": {
        "disease": "Bronchitis",
        "description": "Inflammation of the bronchial tubes causing coughing and mucus production.",
        "prevention": "Avoid smoking, stay hydrated.",
        "diet": "Warm soups, herbal teas.",
        "exercise": "Deep breathing exercises."
    },
        "headache": {
        "disease": "Migraine",
        "description": "Severe headache often accompanied by nausea, light sensitivity, and vomiting.",
        "prevention": "Avoid triggers like stress, loud noises, and certain foods.",
        "diet": "Eat regular meals, stay hydrated.",
        "exercise": "Gentle yoga or meditation."
    },
    "skin_rash": {
        "disease": "Eczema",
        "description": "A condition causing inflamed, itchy, and cracked skin.",
        "prevention": "Use gentle soaps, moisturize regularly, avoid allergens.",
        "diet": "Omega-3 rich foods like fish and flaxseeds.",
        "exercise": "Low-impact activities to avoid sweating."
    },
    "fatigue": {
        "disease": "Anemia",
        "description": "A condition characterized by low red blood cell count leading to fatigue.",
        "prevention": "Eat iron-rich foods, treat underlying causes.",
        "diet": "Leafy greens, lean meats, beans.",
        "exercise": "Light aerobic activities like walking."
    },
    "shortness_of_breath": {
        "disease": "Asthma",
        "description": "Chronic inflammation of the airways causing difficulty breathing.",
        "prevention": "Avoid allergens, manage stress.",
        "diet": "Anti-inflammatory foods like ginger and turmeric.",
        "exercise": "Breathing exercises or swimming."
    },
    "chest_pain": {
        "disease": "Angina",
        "description": "Chest pain caused by reduced blood flow to the heart.",
        "prevention": "Maintain a healthy weight, avoid high-fat diets.",
        "diet": "Low-fat, heart-healthy foods.",
        "exercise": "Light walking or guided cardiac rehabilitation exercises."
    },
    "itching": {
        "disease": "Fungal Infection",
        "description": "A skin infection caused by fungi, leading to itching and redness.",
        "prevention": "Keep skin clean and dry, avoid sharing personal items.",
        "diet": "Probiotic-rich foods like yogurt.",
        "exercise": "Avoid activities causing excessive sweating."
    },
    "sore_throat": {
        "disease": "Pharyngitis",
        "description": "Inflammation of the throat causing pain and discomfort.",
        "prevention": "Avoid cold drinks, stay hydrated.",
        "diet": "Warm teas with honey, soups.",
        "exercise": "Rest and avoid strenuous activities."
    },
    "joint_pain": {
        "disease": "Arthritis",
        "description": "Inflammation of joints causing pain and stiffness.",
        "prevention": "Maintain a healthy weight, stay active.",
        "diet": "Foods rich in omega-3 fatty acids.",
        "exercise": "Low-impact exercises like swimming or cycling."
    },
    "vomiting": {
        "disease": "Gastroenteritis",
        "description": "Inflammation of the stomach and intestines causing vomiting and diarrhea.",
        "prevention": "Avoid contaminated food and water.",
        "diet": "Eat bananas, rice, applesauce, and toast (BRAT diet).",
        "exercise": "Rest and avoid physical activities."
    },
    "runny_nose": {
        "disease": "Allergic Rhinitis",
        "description": "An allergic reaction causing sneezing, runny nose, and congestion.",
        "prevention": "Avoid allergens like dust and pollen.",
        "diet": "Foods rich in Vitamin C to boost immunity.",
        "exercise": "Indoor activities during high pollen seasons."
    },
    "dizziness": {
        "disease": "Vertigo",
        "description": "A sensation of spinning or loss of balance caused by inner ear issues.",
        "prevention": "Avoid sudden movements, stay hydrated.",
        "diet": "Reduce salt intake to prevent fluid retention.",
        "exercise": "Balance exercises and physical therapy."
    },
    "nausea": {
        "disease": "Motion Sickness",
        "description": "A condition causing nausea due to movement during travel.",
        "prevention": "Avoid heavy meals before traveling, focus on a fixed point.",
        "diet": "Ginger tea or peppermint.",
        "exercise": "Focus on deep breathing exercises."
    },
    "blurred_vision": {
        "disease": "Glaucoma",
        "description": "A condition leading to increased pressure in the eyes, affecting vision.",
        "prevention": "Regular eye check-ups, avoid eye strain.",
        "diet": "Foods rich in antioxidants like carrots and spinach.",
        "exercise": "Walking or yoga to reduce stress."
    }
}

# Twilio configuration
ACCOUNT_SID = "ACbb00aa7fc73767e8d4cc03ca42d60723"
AUTH_TOKEN = "6aa60accccee8189e1d8d5569d253f24"
TWILIO_NUMBER = "+13257701907"

# Functions
def predict_disease(symptom):
    if symptom in disease_data:
        return disease_data[symptom]
    return {"error": "No matching disease found for the given symptom."}

# Function to save uploaded files
def save_document(file):
    filepath = os.path.join(UPLOAD_FOLDER, file.name)
    # Open the file in binary mode and write directly
    with open(filepath, "wb") as f:
        f.write(file.getbuffer())
    # Add file record to the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (filename) VALUES (?)", (file.name,))
    conn.commit()
    conn.close()
    return file.name


# Function to get all documents from the database
def get_documents():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents")
    documents = cursor.fetchall()
    conn.close()
    return documents

# Function to delete a document from file system and database
def delete_document(doc_id, filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    try:
        # Delete file from the system
        if os.path.exists(filepath):
            os.remove(filepath)
        # Delete the corresponding entry from the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def send_sms(to, message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(to=to, from_=TWILIO_NUMBER, body=message)

# Schedule task function
def schedule_task(phone_number, message, scheduled_time):
    def job():
        send_sms(phone_number, message)
        print(f"Sent reminder to {phone_number} at {datetime.now()}")

    # Schedule the task
    schedule.every().day.at(scheduled_time).do(job)
    
    # Run the scheduler in a separate thread to prevent blocking
    while True:
        schedule.run_pending()
        time.sleep(1)

# Streamlit app
st.title("Multi-Functionality App")

# Symptom-based disease prediction
st.header("1. Symptom-Based Disease Prediction")
symptom = st.text_input("Enter your symptom (e.g., fever, cough):")
if st.button("Predict Disease"):
    result = predict_disease(symptom.lower())
    if "error" in result:
        st.error(result["error"])
    else:
        st.success(f"Disease: {result['disease']}")
        st.write(f"Description: {result['description']}")
        st.write(f"Prevention: {result['prevention']}")
        st.write(f"Diet: {result['diet']}")
        st.write(f"Exercise: {result['exercise']}")

# Document management
st.header("2. Document Management")
init_db()

# Uploading documents
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "docx"])
if uploaded_file:
    filename = save_document(uploaded_file)
    st.success(f"File '{filename}' uploaded successfully!")

# Displaying uploaded documents with options to View, Download, or Delete
st.subheader("Uploaded Documents")
documents = get_documents()

if documents:
    for doc in documents:
        col1, col2, col3 = st.columns([3, 1, 1])
        doc_id, filename = doc
        col1.write(filename)  # Display file name

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        if os.path.exists(filepath):  # Ensure file exists
            with col2:
                # Provide a download link for the document
                with open(filepath, "rb") as file:
                    st.download_button(
                        label="View/Download",
                        data=file,
                        file_name=filename,
                        mime=None,  # Let Streamlit infer the MIME type
                        key=f"download_{doc_id}"  # Unique key
                    )
            with col3:
                # Delete button for the document
                if st.button("Delete", key=f"delete_{doc_id}"):
                    if delete_document(doc_id, filename):
                        st.success(f"File '{filename}' deleted successfully!")
                    else:
                        st.error(f"Failed to delete file '{filename}'.")
else:
    st.write("No documents uploaded yet.")

        


# Twilio integration
st.header("4. Twilio SMS Integration")
recipient = st.text_input("Enter recipient's phone number:")
message = st.text_area("Enter your message:")
if st.button("Send SMS"):
    if recipient and message:
        try:
            send_sms(recipient, message)
            st.success("Message sent successfully!")
        except Exception as e:
            st.error(f"Failed to send message: {e}")
    else:
        st.warning("Please provide both recipient number and message.")