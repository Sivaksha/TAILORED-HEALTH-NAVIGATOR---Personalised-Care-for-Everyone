import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_file(file):
    """Saves the uploaded file to the server."""
    filepath = os.path.join(UPLOAD_FOLDER, file.name)
    with open(filepath, "wb") as f:
        f.write(file.read())
    return file.name

def delete_file_from_storage(filename):
    """Deletes a file from the server."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
