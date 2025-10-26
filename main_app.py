import os
import streamlit as st
import sqlite3
from datetime import datetime
import schedule
import requests
import time
from twilio.rest import Client
import threading
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
import pywhatkit as kit
import plotly.express as px

# Set the page config as the first command
st.set_page_config(page_title="Multi-Functionality App", page_icon="🏥", layout="wide")

# Twilio Credentials
ACCOUNT_SID = "ACbb00aa7fc73767e8d4cc03ca42d60723"  # Replace with your Twilio Account SID
AUTH_TOKEN = "6aa60accccee8189e1d8d5569d253f24"    # Replace with your Twilio Auth Token
TWILIO_NUMBER = "+13257701907"                     # Replace with your Twilio Phone Number

# Initialize database and upload folder
DATABASE = "app.db"
UPLOAD_FOLDER = "uploads"  # Define the upload folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



# Get API keys from environment variables
groq_api_key = os.getenv('GROQ_API_KEY')

# Check for missing API keys
if not groq_api_key:
    st.error("Please set GROQ_API_KEY in your environment variables.")
    st.stop()

# Replace "llama-3.1-70b-versatile" with the new model name from Groq's documentation
NEW_MODEL_NAME = "mistral-saba-24b"  # Example, check Groq documentation.
model = ChatGroq(api_key=groq_api_key, model=NEW_MODEL_NAME, temperature=0)
parser = StrOutputParser()
llm = model | parser

def get_disease_info_groq(symptoms):
    """Gets disease information from Groq LLM and formats it for line-by-line display."""
    try:
        prompt = f"""
        I have the following symptoms: {symptoms}.
        Please provide detailed information including:
        Disease: ...
        Description: ...
        Prevention: ...
        Diet: ...
        Exercise: ...
        """
        response = llm.invoke(prompt)
        return {"prediction": response}
    except Exception as e:
        return {"error": f"Groq API Error: {str(e)}"}



# Twilio SMS Functionality
def send_sms(to, message):
    """Send an SMS using Twilio."""
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        client.messages.create(to=to, from_=TWILIO_NUMBER, body=message)
        st.success(f"Reminder sent successfully to {to}!")
    except Exception as e:
        st.error(f"Failed to send reminder: {e}")

def schedule_reminder(phone_number, message, reminder_time):
    """Schedule a reminder via SMS."""
    def job():
        send_sms(phone_number, message)
        st.success(f"Reminder sent to {phone_number} at {datetime.now()}")

    schedule.every().day.at(reminder_time).do(job)
    threading.Thread(target=run_schedule, daemon=True).start()

def run_schedule():
    """Run scheduled tasks."""
    while True:
        schedule.run_pending()
        time.sleep(1)

# Function to schedule PyWhatKit reminder
def schedule_pywhatkit_reminder(phone_number, message, reminder_time_str):
    now = datetime.now()
    reminder_hour, reminder_minute = map(int, reminder_time_str.split(":"))
    
    # Ensure reminder is set for future time
    if (reminder_hour, reminder_minute) <= (now.hour, now.minute):
        st.error("Reminder time must be in the future.")
        return
    
    kit.sendwhatmsg(phone_number, message, reminder_hour, reminder_minute)


def init_db():
    """Initialize the database and create the necessary tables."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Create documents table (Initial basic structure)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT
        )
    """)

    # Check for missing columns in documents table
    cursor.execute("PRAGMA table_info(documents)")
    columns = [col[1] for col in cursor.fetchall()]

    # Add user_id column if missing
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE documents ADD COLUMN user_id INTEGER")

    # Add uploaded_at column if missing
    if "uploaded_at" not in columns:
        cursor.execute("ALTER TABLE documents ADD COLUMN uploaded_at TEXT")

    # Create health_logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            symptom TEXT,
            medication TEXT,
            timestamp DATETIME
        )
    """)

    conn.commit()
    conn.close()

# Initialize the database
init_db()

# User Authentication
def authenticate(username, password):
    """Authenticate a user."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(username, password):
    """Register a new user."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state["username"] = ""  # Empty string to avoid NoneType errors


#loginpage
def login_page():
    """User login and registration page with proper centering in Streamlit."""

    # Streamlit's built-in method to center content
    col1, col2, col3 = st.columns([1, 2, 1])  # Creates three columns, centering the middle one

    with col2:  # Put everything inside the center column
        st.markdown(
            """
            <style>
                .login-title {
                    font-size: 28px;
                    font-weight: bold;
                    color: #ffffff;
                    text-align: center;
                }
                .login-subtitle {
                    font-size: 16px;
                    font-weight: normal;
                    color: #f0f0f0;
                    margin-bottom: 20px;
                }
                .stTextInput>div>div>input {
                    border-radius: 8px;
                    padding: 10px;
                }
                .stButton>button {
                    background-color: #FF8C00;
                    color: white;
                    font-size: 16px;
                    border-radius: 8px;
                    width: 100%;
                    padding: 10px;
                    font-weight: bold;
                }
                .stButton>button:hover {
                    background-color: #FF4500;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Title & Subtitle
        st.markdown('<p class="login-title">🔐 User Authentication</p>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Secure access to your health assistant</p>', unsafe_allow_html=True)

        # Choose between Login and Register
        choice = st.radio("Choose Action", ["Login", "Register"], horizontal=True)

        if choice == "Login":
            st.subheader("🔑 Login to Your Account")
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")

            if st.button("Login"):
                user = authenticate(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user[0]
                    st.session_state.username = username
                    st.success(f"✅ Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

        elif choice == "Register":
            st.subheader("📝 Create a New Account")
            username = st.text_input("👤 New Username")
            password = st.text_input("🔒 New Password", type="password")

            if st.button("Register"):
                if register_user(username, password):
                    st.success("🎉 Registration successful! Please log in.")
                else:
                    st.error("⚠️ Username already exists.")

        st.markdown('</div>', unsafe_allow_html=True)  # Close login container

# Logout Button
def logout():
    """Logs the user out and resets session state."""
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.rerun()

# If not authenticated, show login page
if not st.session_state.authenticated:
    login_page()
    st.stop()


# Logout Button
def logout():
    """Logs the user out and resets session state."""
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.rerun()

# If not authenticated, show login page
if not st.session_state.authenticated:
    login_page()
    st.stop()

# Sidebar Navigation
st.sidebar.title("Navigation🚀")
st.sidebar.success(f"Logged in as User {st.session_state.username}")

app_mode = st.sidebar.radio("Go to", ["Home🏠", "Disease Prediction🩺", "Document Storage📂", "Medication Reminder💊", "Health Dashboard📊"])

# Logout Button
if st.sidebar.button("Logout", key="logout_button"):
    logout()

# Home Page
if app_mode == "Home🏠":
    # Custom Styling
    st.markdown(
        """
        <style>
            .main-title {
                font-size: 50px; /* Increased font size */
                font-weight: bold;
                color: #FF5733; /* Solid Vibrant Orange */
                text-align: center;
                text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.2); /* Soft shadow */
            }
            .sub-text {
                font-size: 25px; /* Increased font size */
                color: #2E86C1; /* Blue shade */
                text-align: center;
                font-style: italic;
            }
            .feature-box {
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                color: white;
                box-shadow: 3px 3px 10px rgba(0,0,0,0.2);
            }
            .feature1 { background: linear-gradient(to right, #FF5733, #FF8D1A); } /* Orange */
            .feature2 { background: linear-gradient(to right, #3498DB, #6DD5FA); } /* Blue */
            .feature3 { background: linear-gradient(to right, #28B463, #58D68D); } /* Green */
            .feature4 { background: linear-gradient(to right, #8E44AD, #C39BD3); } /* Purple */
            .cta {
                font-size: 22px;
                font-weight: bold;
                text-align: center;
                padding: 10px;
                color: #fff;
                background: linear-gradient(to right, #FFC300, #FF5733);
                border-radius: 8px;
                margin-top: 20px;
                box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page Content
    st.markdown('<p class="main-title">🌟 Welcome to the Multi-Functionality App 🌟</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Your all-in-one intelligent health companion!</p>', unsafe_allow_html=True)

    # Feature Highlights
    st.markdown('<div class="feature-box feature1">🔍 <b>Disease Prediction & Personalized Recommendations</b><br> AI-driven insights tailored to you.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box feature2">📁 <b>Document Management</b><br> Securely store and access all your medical records.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box feature3">⏰ <b>Medication Reminders</b><br> Get timely notifications, never miss a dose!</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-box feature4">📊 <b>Health Tracking & Dashboards</b><br> Monitor and visualize your health trends.</div>', unsafe_allow_html=True)

    # Call to Action
    st.markdown('<p class="cta">🚀 Start exploring from the sidebar now!</p>', unsafe_allow_html=True)

elif app_mode == "Disease Prediction🩺":
    st.title("Symptom-Based Disease Prediction🔬")

    symptoms = st.text_input("Enter symptoms (e.g., 'fever, cough'):")
    if st.button("Predict Disease"):
        if symptoms:
            result = get_disease_info_groq(symptoms)
            if "error" in result:
                st.error(result["error"])
            elif "prediction" in result:
                lines = result["prediction"].split('\n')  # Split response into lines
                for line in lines:
                    st.write(line.strip())  # Display each line, removing extra whitespace
            else:
                st.warning("Unexpected response format.")
        else:
            st.warning("Please enter symptoms to proceed.")

elif app_mode == "Document Storage📂":
    st.header("Document Storage📑")
    st.write("Manage and store documents related to healthcare records.")

    # File uploader
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "docx", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Generate a unique filename to prevent overwrites
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Store file metadata in database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Check if user_id and uploaded_at columns exist
        cursor.execute("PRAGMA table_info(documents)")
        columns = [col[1] for col in cursor.fetchall()]

        if "user_id" not in columns or "uploaded_at" not in columns:
            st.error("Database table 'documents' is missing required columns. Please check your schema.")
        else:
            cursor.execute(
                "INSERT INTO documents (user_id, filename, uploaded_at) VALUES (?, ?, ?)",
                (st.session_state.get("user_id", 1), safe_filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

        conn.close()

        

    # Retrieve and display uploaded files
    st.write("📄 Uploaded Files:")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, uploaded_at FROM documents WHERE user_id = ?", (st.session_state.get("user_id", 1),))
    files = cursor.fetchall()
    conn.close()

    if files:
        for file_id, filename, uploaded_at in files:
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # Check if file exists before displaying
            if os.path.exists(file_path):
                with st.expander(f"📁 {filename} (Uploaded on {uploaded_at})"):
                    # Display images
                    if filename.lower().endswith(("png", "jpg", "jpeg")):
                        st.image(file_path, caption=filename, use_column_width=True)

                    # Download button
                    with open(file_path, "rb") as file:
                        st.download_button(label="📥 Download", data=file, file_name=filename, key=f"download_{file_id}")

                    # Delete button
                    if st.button(f"🗑 Delete {filename}", key=f"delete_{file_id}"):
                        os.remove(file_path)  # Delete from storage
                        conn = sqlite3.connect(DATABASE)
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM documents WHERE id = ?", (file_id,))
                        conn.commit()
                        conn.close()
                        st.warning(f"🚮 File '{filename}' deleted successfully!")
                        st.rerun()
            else:
                # Do not display files that are missing
                continue  
    else:
         st.write("📂 No documents uploaded yet.")


elif app_mode == "Medication Reminder💊":
    st.header("Set a Medication Reminder⏰")
    st.write("Set a reminder to get your medication on time!")

    phone_number = st.text_input("Enter phone number (e.g., +1234567890):")
    reminder_time = st.time_input("Set reminder time (HH:MM):")
    message = st.text_area("Enter reminder message:", "This is your medication reminder!")
    
    reminder_option = st.radio("Choose reminder method:", ("SMS", "Whatapp"))
    
    if st.button("Set Reminder"):
        if phone_number and reminder_time and message:
            try:
                reminder_time_str = reminder_time.strftime("%H:%M")
                if reminder_option == "Twilio":
                    schedule_reminder(phone_number, message, reminder_time_str)
                else:
                    schedule_pywhatkit_reminder(phone_number, message, reminder_time_str)
                
                st.success(f"Reminder set for {reminder_time_str} to {phone_number} via {reminder_option}.")
            except Exception as e:
                st.error(f"Failed to set reminder: {e}")
        else:
            st.warning("Please fill in all fields.")

# 5. Health Dashboard
elif app_mode == "Health Dashboard📊":
    st.header("Personalized Health Dashboard📌")
    st.write("Track your symptoms, medications, and health progress over time.")

    user_id = 1  # Placeholder for user ID
    symptom = st.text_input("Enter symptom (e.g., 'fever', 'cough'):")
    medication = st.text_input("Enter medication (e.g., 'paracetamol'):")

    if st.button("Log Health Data"):
        if symptom or medication:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO health_logs (user_id, symptom, medication, timestamp)
                VALUES (?, ?, ?, ?)
            """, (user_id, symptom, medication, timestamp))
            conn.commit()
            conn.close()
            st.success("Health data logged successfully!")
        else:
         st.warning("Please enter a symptom or medication.")

    if st.button("View/Hide Health Log Data"):
        if 'view' not in st.session_state:
            st.session_state['view'] = False
        st.session_state['view'] = not st.session_state['view']

    if st.session_state.get('view', False):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM health_logs WHERE user_id = ?", (user_id,))
        logged_data = cursor.fetchall()
        conn.close()

        if logged_data:
            st.write("### Health Log Data")
            df = pd.DataFrame(logged_data, columns=["ID", "User ID", "Symptom", "Medication", "Timestamp"])
            st.write(df)

            cursor = sqlite3.connect(DATABASE).cursor()
            cursor.execute("SELECT symptom, COUNT(*) FROM health_logs WHERE user_id = ? GROUP BY symptom", (user_id,))
            symptom_data = cursor.fetchall()
            conn.close()

            if symptom_data:
                symptom_df = pd.DataFrame(symptom_data, columns=["Symptom", "Count"])
                fig = px.bar(symptom_df, x="Symptom", y="Count", title="Symptom Tracking Over Time")
                st.plotly_chart(fig)
            else:
              st.write("No health data available yet.")
            
            delete_id = st.text_input("Enter the ID of the record you want to delete:")
            if st.button("Delete Record"):
                if delete_id:
                    conn = sqlite3.connect(DATABASE)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM health_logs WHERE id = ?", (delete_id,))
                    conn.commit()
                    conn.close()
                    st.success(f"Record with ID {delete_id} deleted successfully!")
                else:
                    st.warning("Please enter a valid record ID.")
        else:
            st.write("No health data logged yet.")