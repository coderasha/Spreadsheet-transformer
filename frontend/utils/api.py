import requests

BASE_URL = "http://localhost:8000"


def upload_file(file):
    files = {"file": file}

    response = requests.post(
        f"{BASE_URL}/upload",
        files=files
    )

    return response.json()