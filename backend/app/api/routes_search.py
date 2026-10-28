# app/api/routes_search.py
import traceback
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.services.search_service import hybrid_search

router = APIRouter()


@router.get("/")
async def search_endpoint(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, description="Number of results to return"),
    db: Session = Depends(get_db),
):
    try:
        results = hybrid_search(q, db, limit)
        return {"data": results}
    except Exception as e:
        # CRITICAL: This line forces the terminal to print the exact crash log!
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
