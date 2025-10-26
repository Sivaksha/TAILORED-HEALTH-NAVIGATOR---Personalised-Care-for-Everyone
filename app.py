#app.py

from flask import Flask, request, render_template, send_from_directory, redirect
import os
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
DATABASE = "documents.db"
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
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    # Add file record to the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (filename) VALUES (?)", (file.filename,))
    conn.commit()
    conn.close()
    return file.filename

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

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("file")  # Allow multiple file uploads
        for file in files:
            if file:
                save_document(file)
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents")
    documents = cursor.fetchall()
    conn.close()
    
    return render_template("index.html", documents=documents)

@app.route("/view/<filename>")
def view_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        return "File not found", 404

@app.route("/delete/<int:doc_id>", methods=["POST"])
def delete_file(doc_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM documents WHERE id = ?", (doc_id,))
    doc = cursor.fetchone()
    conn.close()

    if doc:
        filename = doc[0]
        if delete_document(doc_id, filename):
            return redirect("/")
        else:
            return "Error deleting file", 500
    else:
        return "Document not found", 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)