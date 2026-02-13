"""
Abstract base classes for poster implementations.
Defines the interface all platform-specific posters must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class PostPayload:
    """Standardized payload structure for all platforms."""
    platform: str
    title: str
    content: str
    tags: list = None
    metadata: Dict[str, Any] = None


class BasePoster(ABC):
    """
    Abstract base class for platform-specific posters.
    Enforces Single Responsibility Principle:
    Each poster handles ONLY its platform's API interaction.
    """

    def __init__(self, config: Dict[str, Any], logger=None):
        """
        Args:
            config: Platform-specific configuration from config.yaml
            logger: Optional logger instance
        """
        self.config = config
        self.logger = logger
        self.platform = self.__class__.__name__.replace("Poster", "").upper()
        self._validate_config()

    @abstractmethod
    def _validate_config(self):
        """Validate that required config keys are present."""
        pass

    @abstractmethod
    def post(self, payload: PostPayload) -> Dict[str, Any]:
        """
        Post content to the platform.
        
        Args:
            payload: PostPayload with content and metadata
            
        Returns:
            {
                "status": "success" | "error" | "draft",
                "platform": platform_name,
                "url": posted_url (if applicable),
                "error": error_message (if failed),
                "timestamp": ISO timestamp
            }
        """
        pass

    def _log(self, message: str, level: str = "INFO"):
        """Helper for logging."""
        if self.logger:
            getattr(self.logger, level.lower())(message)
        else:
            prefix = f"[{self.platform}] [{level}]"
            print(f"{prefix} {message}")

    def _safe_post(self, post_func, *args, **kwargs) -> Dict[str, Any]:
        """
        Wrapper for safe posting with error handling.
        
        Args:
            post_func: The actual posting function
            *args, **kwargs: Arguments to pass to post_func
            
        Returns:
            Standardized response dict
        """
        try:
            result = post_func(*args, **kwargs)
            return {
                "status": "success",
                "platform": self.platform,
                **result
            }
        except Exception as e:
            self._log(f"Posting failed: {e}", "ERROR")
            return {
                "status": "error",
                "platform": self.platform,
                "error": str(e)
            }
