import sqlite3
import os

DATABASE = "documents.db"

def init_db():
    """Initializes the SQLite database."""
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

def save_document_to_db(filename):
    """Saves a document's metadata to the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (filename) VALUES (?)", (filename,))
    conn.commit()
    conn.close()

def get_documents_from_db():
    """Fetches all documents from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents")
    documents = cursor.fetchall()
    conn.close()
    return documents

def delete_document_from_db(doc_id):
    """Deletes a document's metadata from the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()
