"""
Infrastructure Service
Contains base classes and factory patterns for the system.
"""

from services.infrastructure.base_writer import BaseWriter
from services.infrastructure.base_poster import BasePoster, PostPayload
from services.infrastructure.poster_factory import PosterFactory

__all__ = [
    'BaseWriter',
    'BasePoster',
    'PostPayload',
    'PosterFactory',
]
