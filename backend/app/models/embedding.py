# app/models/embedding.py
from sentence_transformers import SentenceTransformer

# Load local NLP model for text/code embeddings
# all-MiniLM-L6-v2 is fast and highly effective for semantic search
print("Loading SentenceTransformer model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def get_text_embedding(text: str) -> list[float]:
    """Generates a dense vector for the given text."""
    return embedder.encode(text).tolist()
