#agents/twitter_writer.py
"""Twitter content writer. Generates platform-optimized tweets."""

from agents.base_writer import BaseWriter


class TwitterWriter(BaseWriter):
    """Generates Twitter threads with characteristic voice."""
    
    def get_system_prompt(self) -> str:
        """Twitter-specific prompt."""
        return """You are a tech founder on X.

Read the article below and write a sharp opinion thread.
Rules:
- Confident, authoritative tone
- Slightly controversial
- 5–7 tweets
- No emojis
- Hook in first line
- Each tweet under 280 characters"""
    
    def get_max_tokens(self) -> int:
        """Get max tokens from config or default."""
        return self.config.get("max_tokens", 250)


# For backward compatibility: standalone function
def write_twitter(article_text: str) -> str:
    """
    Legacy function interface.
    Creates a writer with injected LLM and returns generated content.
    """
    from agents.llm_engine import LLMEngine
    from utils.config_loader import ConfigLoader
    
    config = ConfigLoader().get_platform_config("twitter")
    llm = LLMEngine()
    writer = TwitterWriter(llm, config)
    return writer.write(article_text)

