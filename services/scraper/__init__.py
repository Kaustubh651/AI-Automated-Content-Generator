"""
News scraping service.
Handles fetching and processing news from various sources.
"""

from services.scraper.news_scraper import scrape_news, scrape_article

__all__ = [
    'scrape_news',
    'scrape_article',
]

