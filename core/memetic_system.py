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
    """
    Gracie Knowledge System Core
    
    A sophisticated memetic learning framework for AI agents.
    """
    
    def __init__(self, config: Optional[KnowledgeConfig] = None):
        """Initialize the knowledge system with optional configuration."""
        self.config = config or KnowledgeConfig()
        self.logger = setup_logger('GracieKnowledge')
        
        # Initialize components
        self.db = DatabaseManager(self.config.db_path)
        self.memory = MemoryManager(enable_faiss=self.config.enable_faiss)
        self.embedding_model = SentenceTransformer(self.config.embedding_model)
        
        # Initialize FAISS index
        self._initialize_faiss()

    def _initialize_faiss(self):
        """Initialize FAISS for vector similarity search."""
        try:
            embeddings = self.memory.get_all_embeddings()
            if embeddings:
                dimension = embeddings[0].shape[0]
                self.faiss_index = faiss.IndexFlatL2(dimension)
                self.faiss_index.add(embeddings)
                self.logger.info(f"FAISS initialized with {len(embeddings)} entries")
        except Exception as e:
            self.logger.error(f"FAISS initialization error: {e}")

    def add_topic(self, topic: Topic) -> bool:
        """
        Add a new topic to the knowledge base.
        
        Args:
            topic (Topic): Topic object containing knowledge information
            
        Returns:
            bool: Success status
        """
        try:
            # Generate embeddings
            embedding = self.embedding_model.encode(topic.definition)
            
            # Store in database and memory
            self.db.store_topic(topic)
            self.memory.add_embedding(embedding, topic.id)
            
            # Update FAISS index
            if self.config.enable_faiss:
                self.faiss_index.add(embedding.reshape(1, -1))
            
            return True
        except Exception as e:
            self.logger.error(f"Error adding topic: {e}")
            return False

    def get_relevant_knowledge(self, query: str, top_k: int = 5) -> List[Topic]:
        """
        Retrieve relevant knowledge based on query.
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            
        Returns:
            List[Topic]: List of relevant topics
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query)
            
            # Search with FAISS
            if self.config.enable_faiss:
                D, I = self.faiss_index.search(
                    query_embedding.reshape(1, -1), 
                    top_k
                )
                topic_ids = [self.memory.get_topic_id(idx) for idx in I[0]]
                return self.db.get_topics_by_ids(topic_ids)
            
            return []
        except Exception as e:
            self.logger.error(f"Error retrieving knowledge: {e}")
            return []

    def update_topic(self, topic: Topic) -> bool:
        """
        Update existing topic in knowledge base.
        
        Args:
            topic (Topic): Updated topic information
            
        Returns:
            bool: Success status
        """
        try:
            # Update database
            success = self.db.update_topic(topic)
            if success:
                # Update embeddings
                embedding = self.embedding_model.encode(topic.definition)
                self.memory.update_embedding(embedding, topic.id)
                
                # Rebuild FAISS index if needed
                if self.config.enable_faiss:
                    self._initialize_faiss()
            
            return success
        except Exception as e:
            self.logger.error(f"Error updating topic: {e}")
            return False

    def get_stats(self) -> Dict:
        """Get system statistics and metrics."""
        try:
            return {
                "total_topics": self.db.get_topic_count(),
                "total_interactions": self.db.get_interaction_count(),
                "memory_usage": self.memory.get_usage_stats(),
                "last_updated": self.db.get_last_update_time()
            }
        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return {}
