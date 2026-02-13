"""
Centralized configuration management.
All configuration access goes through this module.
"""

from shared.config.config_loader import ConfigLoader

# Singleton instance
config_instance = ConfigLoader()

def get_config():
    """Get the global configuration instance."""
    return config_instance

__all__ = [
    'ConfigLoader',
    'get_config',
    'config_instance',
]
