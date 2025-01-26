# gracie/core/memory_manager.py
from typing import List, Optional, Dict
import numpy as np
import faiss

class MemoryManager:
    """Manages memory and embeddings"""
    def __init__(self, enable_faiss: bool = True):
        self.enable_faiss = enable_faiss
        self.embeddings = {}
        self.topic_map = {}
        
    def add_embedding(self, embedding: np.ndarray, topic_id: str):
        self.embeddings[topic_id] = embedding
        self.topic_map[len(self.embeddings) - 1] = topic_id
        
    def get_all_embeddings(self) -> List[np.ndarray]:
        return list(self.embeddings.values())
        
    def get_usage_stats(self) -> Dict:
        return {
            "total_embeddings": len(self.embeddings),
            "memory_size_mb": sum(e.nbytes for e in self.embeddings.values()) / 1024 / 1024
        }
