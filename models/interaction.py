# gracie/models/interaction.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Interaction:
    """Represents an agent interaction"""
    user_input: str
    agent_response: str
    confidence: float
    timestamp: datetime = None
    interaction_id: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.interaction_id is None:
            self.interaction_id = str(uuid.uuid4())
