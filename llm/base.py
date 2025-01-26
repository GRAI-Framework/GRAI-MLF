# gracie/llm/llm_base.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration for LLM providers"""
    provider: str
    model_name: str
    api_key: Optional[str] = None
    max_tokens: int = 2000
    temperature: float = 0.7
    top_p: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0

class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    def __init__(self, config: LLMConfig):
        self.config = config

    @abstractmethod
    async def generate(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate text based on prompt and context"""
        pass

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        pass
