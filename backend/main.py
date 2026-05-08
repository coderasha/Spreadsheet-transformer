from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="Spreadsheet Transformer")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Spreadsheet Transformer API Running"}