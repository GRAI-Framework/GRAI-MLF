# gracie/core/embeddings.py
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingProcessor:
    """Handles text embeddings"""
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        
    def encode(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)
        
    def get_similarity(self, text1: str, text2: str) -> float:
        emb1 = self.encode([text1])[0]
        emb2 = self.encode([text2])[0]
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
