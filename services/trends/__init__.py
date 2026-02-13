"""
Trends Service
Contains trend analysis and memory management.
"""

from services.trends.trend_memory import load_memory, update_memory, init_memory
from services.trends.trend_evolution import analyze_trend_evolution
from services.trends.trend_bias_engine import apply_trend_bias

__all__ = [
    'load_memory',
    'update_memory',
    'init_memory',
    'analyze_trend_evolution',
    'apply_trend_bias',
]
