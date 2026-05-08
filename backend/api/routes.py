from fastapi import APIRouter, UploadFile, File
from backend.services.file_service import save_uploaded_file
from backend.parsers.excel_parser import read_excel

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = await save_uploaded_file(file)
    df = read_excel(file_path)

    return {
        "columns": list(df.columns),
        "rows": df.head(100).to_dict(orient="records")
    }