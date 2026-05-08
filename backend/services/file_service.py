import os

UPLOAD_DIR = "storage/uploads"

async def save_uploaded_file(file):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return file_path