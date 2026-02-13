# utils/config_loader.py
"""
Centralized configuration management.
Single Responsibility: Load, validate, and provide config across the application.
No hard-coded values outside this module.
"""

import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import os


class ConfigLoader:
    """Configuration manager with lazy loading and validation."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """Singleton pattern: Only one config instance."""
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize config paths."""
        if self._config is None:
            self.config_path = Path("config/config.yaml")
            self.secrets_path = Path("config/secrets.env")
            self._load_all()
    
    def _load_all(self):
        """Load and merge all config sources."""
        # Load environment secrets first
        if self.secrets_path.exists():
            load_dotenv(str(self.secrets_path))
        
        # Load YAML config
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, "r") as f:
            ConfigLoader._config = yaml.safe_load(f)
        
        # Validate required sections
        self._validate()
    
    def _validate(self):
        """Validate config structure."""
        required_keys = ["model", "platforms"]
        for key in required_keys:
            if key not in self._config:
                raise ValueError(f"Missing required config key: {key}")
    
    def get(self, key_path: str, default=None) -> Any:
        """
        Get config value using dot notation.
        
        Args:
            key_path: "section.subsection.key" format
            default: Default value if key not found
            
        Returns:
            Config value or default
        """
        keys = key_path.split(".")
        value = self._config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire config dictionary."""
        return self._config.copy()
    
    def get_env(self, key: str, default=None) -> str:
        """Get environment variable with default."""
        return os.getenv(key, default)
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration section."""
        return self.get("model", {})
    
    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """Get platform-specific configuration."""
        return self.get(f"platforms.{platform}", {})
    
    def is_live_mode(self) -> bool:
        """Check if live posting is enabled."""
        return self.get("posting.live_mode", False)
    
    def get_enabled_platforms(self) -> list:
        """Get list of enabled platforms."""
        return self.get("posting.enabled_platforms", [])


# Convenience function for backward compatibility
def load_config() -> Dict[str, Any]:
    """Load and return entire config dictionary."""
    return ConfigLoader().get_all()
