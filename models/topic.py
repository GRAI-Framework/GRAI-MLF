# gracie/models/topic.py
from dataclasses import dataclass
from typing import List, Optional
import uuid

@dataclass
class Topic:
    """Represents a knowledge topic"""
    name: str
    definition: str
    facts: List[str]
    confidence: float = 0.0
    id: str = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
