# gracie/utils/validators.py
from typing import Any, Dict, List
import re

class Validator:
    """Validation utilities"""
    @staticmethod
    def validate_topic(topic_data: Dict[str, Any]) -> bool:
        """Validate topic data"""
        required_fields = ['name', 'definition']
        return all(field in topic_data for field in required_fields)
    
    @staticmethod
    def validate_embedding_input(text: str) -> bool:
        """Validate text for embedding generation"""
        if not text or not isinstance(text, str):
            return False
        return len(text.strip()) > 0
        
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize input text"""
        # Remove special characters
        text = re.sub(r'[^\w\s\-\.]', '', text)
        # Remove extra whitespace
        return ' '.join(text.split())
