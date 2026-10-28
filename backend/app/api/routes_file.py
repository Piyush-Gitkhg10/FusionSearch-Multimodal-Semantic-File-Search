# app/api/routes_file.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.services.file_service import process_local_folder

router = APIRouter()


class FolderPathRequest(BaseModel):
    folder_path: str


@router.post("/index-folder")
async def index_local_folder(req: FolderPathRequest, db: Session = Depends(get_db)):
    # Automatically remove literal double or single quotes added by Windows File Explorer
    clean_path = req.folder_path.strip('"').strip("'")

    try:
        results = process_local_folder(clean_path, db)
        return {"message": "Folder indexing complete.", "details": results}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
