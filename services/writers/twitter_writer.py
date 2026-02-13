#services/writers/twitter_writer.py
"""Twitter content writer. Generates platform-optimized tweets."""

from services.infrastructure.base_writer import BaseWriter


class TwitterWriter(BaseWriter):
    """Generates Twitter threads with characteristic voice."""
    
    def get_system_prompt(self) -> str:
        """Twitter-specific prompt."""
        return """You are a tech founder on X.

Read the article below and write a sharp opinion thread.
Rules:
- Max 280 characters per tweet
- Use emojis sparingly
- Quote statistics for credibility
- End with a question to drive engagement

Keep it punchy, actionable, and authentic."""
    
    def get_max_tokens(self) -> int:
        """Get max tokens from config or default."""
        return self.config.get("max_tokens", 256)


# For backward compatibility: standalone function
def write_twitter(article_text: str) -> str:
    """
    Legacy function interface.
    Creates a writer with injected LLM and returns generated content.
    """
    from services.meme_engine.llm_engine import LLMEngine
    from shared.config import get_config
    
    config = get_config().get_platform_config("twitter")
    llm = LLMEngine()
    writer = TwitterWriter(llm, config)
    return writer.write(article_text)

