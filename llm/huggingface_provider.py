# gracie/integrations/huggingface_provider.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import Dict, List, Optional
from .llm_base import BaseLLMProvider, LLMConfig

class HuggingFaceProvider(BaseLLMProvider):
    """HuggingFace integration"""
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(config.model_name)
        if torch.cuda.is_available():
            self.model = self.model.to('cuda')

    async def generate(self, prompt: str, context: Optional[Dict] = None) -> str:
        try:
            # Prepare input text
            input_text = prompt
            if context and context.get('system_prompt'):
                input_text = f"{context['system_prompt']}\n\n{prompt}"

            inputs = self.tokenizer(input_text, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = inputs.to('cuda')

            # Generate response
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                num_return_sequences=1
            )

            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        except Exception as e:
            raise Exception(f"HuggingFace generation error: {str(e)}")

    async def embed(self, text: str) -> List[float]:
        try:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            if torch.cuda.is_available():
                inputs = inputs.to('cuda')
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Use the last hidden state as embedding
            embeddings = outputs.last_hidden_state.mean(dim=1)
            return embeddings[0].cpu().numpy().tolist()
        except Exception as e:
            raise Exception(f"HuggingFace embedding error: {str(e)}")
