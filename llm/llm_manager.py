# gracie/integrations/llm_manager.py
from typing import Dict, Optional
from .llm_base import LLMConfig, BaseLLMProvider
from .openai_provider import OpenAIProvider
from .huggingface_provider import HuggingFaceProvider

class LLMManager:
    """Manages LLM integrations"""
    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {}

    def add_provider(self, config: LLMConfig) -> None:
        """Add a new LLM provider"""
        if config.provider.lower() == "openai":
            self.providers[config.provider] = OpenAIProvider(config)
        elif config.provider.lower() == "huggingface":
            self.providers[config.provider] = HuggingFaceProvider(config)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")

    async def generate(self, provider: str, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate text using specified provider"""
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not configured")
        return await self.providers[provider].generate(prompt, context)

    async def embed(self, provider: str, text: str) -> List[float]:
        """Generate embeddings using specified provider"""
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not configured")
        return await self.providers[provider].embed(text)
