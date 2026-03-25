from fastapi import APIRouter, UploadFile, File, HTTPException
from app.agents.file_agent import FileAgent
from typing import List

router = APIRouter(prefix="/api/files", tags=["files"])
file_agent = FileAgent()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传文件"""
    try:
        content = await file.read()
        result = file_agent.upload_file(content, file.filename)
        return {"status": "ok", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/parse")
async def parse_file(file_path: str, format: str = "csv", sheet_name: str = "0"):
    """解析文件"""
    try:
        if format == "csv":
            df = file_agent.parse_csv(file_path)
        elif format == "excel":
            df = file_agent.parse_excel(file_path, sheet_name)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")

        schema = file_agent.get_schema(df)
        return schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))