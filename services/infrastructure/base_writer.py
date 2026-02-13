"""
Abstract base classes for content writers.
Separates content GENERATION from content POSTING.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseWriter(ABC):
    """
    Abstract base class for platform-specific content writers.
    Single Responsibility: Generate platform-optimized content from raw article text.
    """

    def __init__(self, llm_engine, config: Dict[str, Any], logger=None):
        """
        Args:
            llm_engine: Injected LLM instance (dependency injection)
            config: Platform-specific writer config
            logger: Optional logger
        """
        self.llm_engine = llm_engine
        self.config = config
        self.logger = logger
        self.platform = self.__class__.__name__.replace("Writer", "").upper()

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this platform."""
        pass

    @abstractmethod
    def get_max_tokens(self) -> int:
        """Return max tokens for this platform's content."""
        pass

    def write(self, article_text: str) -> str:
        """
        Generate platform-specific content.
        
        Args:
            article_text: Raw article or context
            
        Returns:
            Platform-optimized content
        """
        prompt = f"""{self.get_system_prompt()}

Article:
{article_text}"""
        
        return self.llm_engine.generate(
            prompt,
            max_new_tokens=self.get_max_tokens()
        )

    def _log(self, message: str):
        """Helper for logging."""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[{self.platform} WRITER] {message}")
