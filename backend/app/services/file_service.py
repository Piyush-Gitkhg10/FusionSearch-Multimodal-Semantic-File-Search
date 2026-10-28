# app/services/file_service.py
import os
import logging
from pathlib import Path
from sqlalchemy.orm import Session
from app.database.models import FileRecord
from app.models.embedding import get_text_embedding
from app.vector_store.faiss_manager import faiss_manager
from app.services.gemini_service import generate_image_caption

logger = logging.getLogger(__name__)

# Define what we care about
SUPPORTED_EXTS = {
    "text_or_code": [
        ".txt",
        ".md",
        ".py",
        ".js",
        ".java",
        ".cpp",
        ".json",
        ".html",
        ".css",
        ".ino",
    ],
    "image": [".jpg", ".jpeg", ".png"],
}


def process_local_folder(folder_path: str, db_session: Session) -> dict:
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        raise ValueError(f"Directory not found: {folder_path}")

    indexed_count = 0
    skipped_count = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            ext = Path(file).suffix.lower()

            # Skip if already in database
            existing = (
                db_session.query(FileRecord).filter_by(file_path=file_path).first()
            )
            if existing:
                skipped_count += 1
                continue

            summary = ""
            file_type = "unknown"

            try:
                # Handle Code and Text Files
                if ext in SUPPORTED_EXTS["text_or_code"]:
                    file_type = "text/code"
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        # For massive files, you'd chunk this. For now, read the first 2000 chars.
                        summary = f.read()[:2000]

                # Handle Image Files
                elif ext in SUPPORTED_EXTS["image"]:
                    file_type = "image"
                    summary = generate_image_caption(file_path)

                else:
                    skipped_count += 1
                    continue

                # 1. Create DB Record to get the FAISS ID
                new_record = FileRecord(
                    file_name=file,
                    file_path=file_path,
                    file_type=file_type,
                    summary=summary,
                )
                db_session.add(new_record)
                db_session.commit()
                db_session.refresh(new_record)

                # 2. Generate Embedding & Save to FAISS
                embedding_vector = get_text_embedding(summary)
                faiss_manager.add_vector(embedding_vector, new_record.faiss_id)

                indexed_count += 1
                logger.info(f"Indexed: {file}")

            except Exception as e:
                logger.error(f"Failed to process {file}: {e}")
                db_session.rollback()

    return {"indexed": indexed_count, "skipped": skipped_count}
