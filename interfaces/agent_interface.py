# gracie/interfaces/agent_interface.py
from typing import List, Optional, Dict
from ..core.knowledge_system import GracieKnowledgeSystem, KnowledgeConfig
from ..models.topic import Topic
from ..utils.logger import setup_logger

class Agent:
    """Base agent interface"""
    def __init__(
        self,
        name: str,
        knowledge_config: Optional[KnowledgeConfig] = None,
        personality_traits: List[Dict] = None,
        memory_retention: float = 0.8
    ):
        self.name = name
        self.logger = setup_logger(f"Agent_{name}")
        self.knowledge = GracieKnowledgeSystem(knowledge_config)
        self.personality_traits = personality_traits or []
        self.memory_retention = memory_retention
        
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        try:
            # Get relevant knowledge
            knowledge = self.knowledge.get_relevant_knowledge(user_input)
            
            # Apply personality traits
            # This is where you'd integrate with your LLM
            response = f"Agent {self.name} processed: {user_input}"
            
            return response
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            return f"Error processing input: {str(e)}"
            
    def add_knowledge(self, topics: List[Topic]):
        """Add new knowledge to the agent"""
        for topic in topics:
            self.knowledge.add_topic(topic)
            
    def get_stats(self) -> Dict:
        """Get agent statistics"""
        return self.knowledge.get_stats()
