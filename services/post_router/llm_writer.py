# services/post_router/llm_writer.py
"""
Lightweight adapter to use LLM directly for simple prompt-response flows.
"""
from services.meme_engine.llm_engine import LLMEngine
from shared.config.config_loader import ConfigLoader


def generate_simple(prompt: str, max_tokens: int = None) -> str:
    config = ConfigLoader().get_model_config()
    engine = LLMEngine(config=config)
    return engine.generate(prompt, max_new_tokens=max_tokens)
