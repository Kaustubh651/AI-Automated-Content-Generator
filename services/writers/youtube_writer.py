#services/writers/youtube_writer.py
"""YouTube content writer. Generates short video scripts."""

from services.infrastructure.base_writer import BaseWriter


class YouTubeWriter(BaseWriter):
    """Generates YouTube-optimized video scripts."""
    
    def get_system_prompt(self) -> str:
        """YouTube-specific prompt."""
        return """You are an engaging tech YouTuber.

Write a 60–90 second video script.
Rules:
- Strong, attention-grabbing hook (first 5 seconds crucial)
- Clear explanation of impact on industry
- Simple, conversational language
- End with clear call to action (subscribe/like/comment)
- Natural pacing and pauses"""
    
    def get_max_tokens(self) -> int:
        """Get max tokens from config or default."""
        return self.config.get("max_tokens", 500)


# For backward compatibility: standalone function
def write_youtube(article_text: str) -> str:
    """
    Legacy function interface.
    Creates a writer with injected LLM and returns generated content.
    """
    from services.meme_engine.llm_engine import LLMEngine
    from shared.config import get_config
    
    config = get_config().get_platform_config("youtube")
    llm = LLMEngine()
    writer = YouTubeWriter(llm, config)
    return writer.write(article_text)

