"""
Data Service
Contains data collection and analysis modules.
"""

from services.data.market_signal_collector import collect_market_signals
from services.data.market_signal_scorer import score_signals
from services.data.news_scraper import scrape_news

__all__ = [
    'collect_market_signals',
    'score_signals',
    'scrape_news',
]
