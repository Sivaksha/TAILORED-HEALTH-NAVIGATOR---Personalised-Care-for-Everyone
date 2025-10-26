#document management.py

import os
import sqlite3
import streamlit as st

DATABASE = "documents.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the database (if not already initialized)
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

# Function to save uploaded files
def save_document(file):
    filepath = os.path.join(UPLOAD_FOLDER, file.name)
    with open(filepath, "wb") as f:
        f.write(file.read())
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

# Streamlit UI

st.title("Document Management")

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
        doc_id, filename = doc
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Ensure file exists before showing it
        if not os.path.exists(filepath):
            # File is missing, remove it from the database
            delete_document(doc_id, filename)
            continue
        
        # Display the document
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(filename)
        
        with col2:
            # Provide a download link to view the document
            with open(filepath, "rb") as file:
                st.download_button(
                    label="View/Download",
                    data=file,
                    file_name=filename
                )
        
        with col3:
            # Delete button for the document
            if st.button(f"Delete", key=f"delete_{doc_id}"):
                if delete_document(doc_id, filename):
                    st.success(f"File '{filename}' deleted successfully!")
                else:
                    st.error(f"Failed to delete file '{filename}'")

else:
    st.write("No documents uploaded yet.")