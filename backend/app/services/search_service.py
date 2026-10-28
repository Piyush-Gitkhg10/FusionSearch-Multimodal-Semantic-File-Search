# app/services/search_service.py
import logging
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import FileRecord
from app.models.embedding import get_text_embedding
from app.vector_store.faiss_manager import faiss_manager

logger = logging.getLogger(__name__)


def hybrid_search(query: str, db: Session, limit: int = 10):
    logger.info(f"Executing hybrid search for: '{query}'")

    # 1. Semantic Search (FAISS)
    query_vector = get_text_embedding(query)
    # Ensure it's explicitly a float32 numpy array for FAISS
    query_vector_np = np.array([query_vector], dtype=np.float32)

    distances, indices = faiss_manager.index.search(query_vector_np, limit)

    semantic_results = {}
    if len(indices) > 0:
        for i, faiss_id in enumerate(indices[0]):
            # CRITICAL FIX: Ignore FAISS padding (-1)
            if faiss_id == -1:
                continue
            # Convert distance to a similarity score (closer to 1 is better)
            semantic_results[int(faiss_id)] = 1.0 / (1.0 + float(distances[0][i]))

    # 2. Keyword Search (PostgreSQL pg_trgm)
    keyword_results = {}
    try:
        # We query the database to get matching filenames using trigram similarity
        db_results = (
            db.query(
                FileRecord.faiss_id,
                func.similarity(FileRecord.file_name, query).label("sim_score"),
            )
            .filter(FileRecord.faiss_id.in_(list(semantic_results.keys())))
            .all()
        )

        for record in db_results:
            if record.faiss_id is not None:
                keyword_results[record.faiss_id] = float(record.sim_score or 0.0)
    except Exception as e:
        logger.error(f"PostgreSQL Keyword Search Failed: {e}")
        # CRITICAL FIX: Roll back the aborted transaction so the next query can run!
        db.rollback()

    # 3. Combine and Normalize Scores
    final_results = []

    # Fetch actual file metadata from DB
    valid_faiss_ids = list(semantic_results.keys())
    if not valid_faiss_ids:
        return []

    files = db.query(FileRecord).filter(FileRecord.faiss_id.in_(valid_faiss_ids)).all()

    for file in files:
        sem_score = semantic_results.get(file.faiss_id, 0.0)
        key_score = keyword_results.get(file.faiss_id, 0.0)

        # Weighted combination: 70% Semantic context, 30% Keyword filename match
        final_score = (sem_score * 0.7) + (key_score * 0.3)

        final_results.append(
            {
                "id": str(file.id),
                "file_name": file.file_name,
                "file_type": file.file_type,
                "snippet": (
                    file.summary[:200] + "..."
                    if file.summary
                    else "No summary available."
                ),
                "scores": {
                    "semantic_score": sem_score,
                    "filename_score": key_score,
                    "final_score": final_score,
                },
            }
        )

    # Sort by highest final score
    final_results.sort(key=lambda x: x["scores"]["final_score"], reverse=True)
    return final_results[:limit]
