# agents/llm_engine.py
"""
Language Model Engine.
Single Responsibility: Load and manage LLM for text generation.
All model config comes from config.yaml, not hard-coded.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from utils.config_loader import ConfigLoader


class LLMEngine:
    """
    Manages LLM model loading and inference.
    Uses dependency injection: config is injected, not hard-coded.
    """
    
    def __init__(self, config=None, logger=None):
        """
        Args:
            config: Optional config dict. If None, loads from ConfigLoader.
            logger: Optional logger instance.
        """
        self.logger = logger
        self.config = config or ConfigLoader().get_model_config()
        self.model = None
        self.tokenizer = None
        self.device = None
        
        self._load_model()
    
    def _load_model(self):
        """Load model from config."""
        model_name = self.config.get("name", "gpt2")
        self._log(f"Loading model: {model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            ).to(self.device)
            
            self._log(f"Model loaded successfully on {self.device}")
        except Exception as e:
            self._log(f"Failed to load model: {e}", "ERROR")
            raise
    
    def generate(self, prompt: str, max_new_tokens: int = None) -> str:
        """
        Generate text from prompt.
        
        Args:
            prompt: Input prompt
            max_new_tokens: Max tokens to generate (uses config default if None)
            
        Returns:
            Generated text
        """
        if max_new_tokens is None:
            max_new_tokens = self.config.get("max_tokens", 512)
        
        temperature = self.config.get("temperature", 0.7)
        top_p = self.config.get("top_p", 0.95)
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=top_p
            )
            
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            self._log(f"Generation failed: {e}", "ERROR")
            raise
    
    def _log(self, message: str, level: str = "INFO"):
        """Helper for logging."""
        if self.logger:
            getattr(self.logger, level.lower())(message)
        else:
            print(f"[LLM] [{level}] {message}")

