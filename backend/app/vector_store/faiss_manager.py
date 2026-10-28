# app/vector_store/faiss_manager.py
import faiss
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

INDEX_DIR = "app/vector_store/index"
INDEX_PATH = os.path.join(INDEX_DIR, "faiss_index.bin")
VECTOR_DIMENSION = 384  # Specific to all-MiniLM-L6-v2


class FAISSManager:
    def __init__(self):
        self.dimension = VECTOR_DIMENSION
        self.index = self._load_or_create_index()

    def _load_or_create_index(self):
        """Loads the index from disk if it exists, otherwise creates a new one."""
        if os.path.exists(INDEX_PATH):
            logger.info(f"Loading existing FAISS index from {INDEX_PATH}")
            return faiss.read_index(INDEX_PATH)

        logger.info("Creating new FAISS IndexIDMap.")
        # IndexFlatL2 measures the L2 (Euclidean) distance between vectors
        base_index = faiss.IndexFlatL2(self.dimension)
        # Wrap it in IndexIDMap to allow custom integer IDs
        return faiss.IndexIDMap(base_index)

    def add_vector(self, vector: list[float], faiss_id: int):
        """Adds a single vector to the index with its corresponding DB integer ID."""
        # FAISS requires numpy arrays of type float32 and shape (n, d)
        np_vector = np.array([vector], dtype=np.float32)
        np_id = np.array([faiss_id], dtype=np.int64)

        self.index.add_with_ids(np_vector, np_id)
        self.save_index()
        logger.info(f"Added vector for FAISS ID: {faiss_id}")

    def search_vectors(self, query_vector: list[float], top_k: int = 5):
        """
        Searches the index for the closest vectors.
        Returns a tuple of (distances, faiss_ids).
        """
        if self.index.ntotal == 0:
            return [], []

        np_query = np.array([query_vector], dtype=np.float32)
        distances, indices = self.index.search(np_query, top_k)

        # Flatten the results
        return distances[0].tolist(), indices[0].tolist()

    def save_index(self):
        """Persists the in-memory index to disk."""
        os.makedirs(INDEX_DIR, exist_ok=True)
        faiss.write_index(self.index, INDEX_PATH)


# Instantiate a singleton to be used across the app
faiss_manager = FAISSManager()
