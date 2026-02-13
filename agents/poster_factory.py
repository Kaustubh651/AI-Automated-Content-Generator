"""
Poster Factory: Creates poster instances with dependency injection.
Pattern: Factory Pattern for loose coupling.
Single Responsibility: Instantiate correct poster based on platform.
"""

from typing import Dict, Type
from agents.base_poster import BasePoster
from utils.config_loader import ConfigLoader


class PosterFactory:
    """
    Factory for creating platform-specific poster instances.
    Ensures proper dependency injection and loose coupling.
    """
    
    _posters: Dict[str, Type[BasePoster]] = {}
    
    @classmethod
    def register(cls, platform: str, poster_class: Type[BasePoster]):
        """
        Register a poster class for a platform.
        
        Args:
            platform: Platform name (e.g., 'twitter', 'medium')
            poster_class: Poster class (must extend BasePoster)
        """
        if not issubclass(poster_class, BasePoster):
            raise TypeError(f"{poster_class} must extend BasePoster")
        cls._posters[platform.lower()] = poster_class
    
    @classmethod
    def create(cls, platform: str, logger=None) -> BasePoster:
        """
        Create a poster instance for the given platform.
        
        Args:
            platform: Platform name
            logger: Optional logger instance
            
        Returns:
            Initialized poster instance
            
        Raises:
            ValueError: If platform not registered
        """
        platform = platform.lower()
        
        if platform not in cls._posters:
            raise ValueError(
                f"Unknown platform: {platform}. "
                f"Available: {list(cls._posters.keys())}"
            )
        
        # Get platform config
        config_loader = ConfigLoader()
        config = config_loader.get_platform_config(platform)
        
        # Instantiate poster with injected config
        poster_class = cls._posters[platform]
        return poster_class(config=config, logger=logger)
    
    @classmethod
    def get_available_posters(cls) -> list:
        """Get list of registered poster platforms."""
        return list(cls._posters.keys())


# Auto-register built-in posters
def _register_builtin_posters():
    """Register all built-in poster implementations."""
    try:
        from agents.twitter_poster import TwitterPoster
        PosterFactory.register("twitter", TwitterPoster)
    except ImportError:
        pass
    
    try:
        from agents.medium_poster import MediumPoster
        PosterFactory.register("medium", MediumPoster)
    except ImportError:
        pass
    
    try:
        from agents.youtube_poster import YouTubePoster
        PosterFactory.register("youtube", YouTubePoster)
    except ImportError:
        pass
    
    try:
        from agents.instagram_poster import InstagramPoster
        PosterFactory.register("instagram", InstagramPoster)
    except ImportError:
        pass


# Auto-register on module import
_register_builtin_posters()
