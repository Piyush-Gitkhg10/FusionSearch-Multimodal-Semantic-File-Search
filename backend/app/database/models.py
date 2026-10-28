# app/database/models.py
import uuid
from datetime import datetime

# FIX: Added Identity to the import list
from sqlalchemy import Column, String, Text, DateTime, BigInteger, Identity
from sqlalchemy.dialects.postgresql import UUID
from app.database.postgres import Base


class FileRecord(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # FIX: Use Identity(start=1) to force PostgreSQL to auto-increment a non-primary key
    faiss_id = Column(BigInteger, Identity(start=1), unique=True, index=True)

    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False, unique=True)
    file_type = Column(String(50), nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FileRecord(file_name='{self.file_name}', type='{self.file_type}')>"
