"""
Data payload schemas used across services.
Provides standardized data contracts.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class PostPayload:
    """Standard format for posting to platforms."""
    content: str
    platform: str  # 'twitter', 'medium', 'youtube', 'instagram'
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContentPayload:
    """Standard format for generated content."""
    original_article: str
    platform: str
    generated_content: str
    style: str  # 'casual', 'technical', 'marketing'
    quality_score: float = 0.0
    timestamp: Optional[str] = None


@dataclass
class SignalPayload:
    """Market signal data structure."""
    topic: str
    signal_type: str  # 'trending', 'viral', 'news', 'opinion'
    score: float
    source: str
    timestamp: str
    related_content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
