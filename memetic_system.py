# gracie/core/memetic_system.py
from typing import Dict, List, Optional
from dataclasses import dataclass
import faiss
from sentence_transformers import SentenceTransformer
from .database import DatabaseManager
from .memory_manager import MemoryManager
from ..models.topic import Topic
from ..utils.logger import setup_logger

@dataclass
class KnowledgeConfig:
    """Configuration for the Knowledge System"""
    embedding_model: str = "all-MiniLM-L6-v2"
    db_path: str = "gracie_knowledge.db"
    enable_faiss: bool = True
    max_contexts: int = 5
    confidence_threshold: float = 0.7

class GracieKnowledgeSystem:
    """Core knowledge system implementation"""
    def __init__(self, config: Optional[KnowledgeConfig] = None):
        self.config = config or KnowledgeConfig()
        self.logger = setup_logger('GracieKnowledge')
        self.db = DatabaseManager(self.config.db_path)
        self.memory = MemoryManager(enable_faiss=self.config.enable_faiss)
        self.embedding_model = SentenceTransformer(self.config.embedding_model)
        self._initialize_faiss()

    # ... (rest of implementation as shown before)

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

# gracie/core/database.py
import sqlite3
from typing import List, Optional
from ..models.topic import Topic

class DatabaseManager:
    """Manages SQLite database operations"""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_db()
        
    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS topics (
                    id TEXT PRIMARY KEY,
                    name TEXT UNIQUE,
                    definition TEXT,
                    facts TEXT,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Add other necessary tables
            
    def store_topic(self, topic: Topic) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO topics (id, name, definition, facts, confidence) VALUES (?, ?, ?, ?, ?)",
                    (topic.id, topic.name, topic.definition, str(topic.facts), topic.confidence)
                )
                return True
        except Exception:
            return False
