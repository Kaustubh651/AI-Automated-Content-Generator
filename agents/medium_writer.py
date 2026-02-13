#agents/medium_writer.py
"""Medium blog content writer. Generates analytical long-form articles."""

from agents.base_writer import BaseWriter


class MediumWriter(BaseWriter):
    """Generates Medium-optimized blog posts."""
    
    def get_system_prompt(self) -> str:
        """Medium-specific prompt."""
        return """You are a tech blogger writing for Medium.

Write a thoughtful, analytical article.
Structure:
- Title (compelling)
- Brief introduction
- 3 main sections with headings
- Practical conclusion with actionable insights

Tone: analytical, clear, engaging, human."""
    
    def get_max_tokens(self) -> int:
        """Get max tokens from config or default."""
        return self.config.get("max_tokens", 600)


# For backward compatibility: standalone function
def write_medium(article_text: str) -> str:
    """
    Legacy function interface.
    Creates a writer with injected LLM and returns generated content.
    """
    from agents.llm_engine import LLMEngine
    from utils.config_loader import ConfigLoader
    
    config = ConfigLoader().get_platform_config("medium")
    llm = LLMEngine()
    writer = MediumWriter(llm, config)
    return writer.write(article_text)

