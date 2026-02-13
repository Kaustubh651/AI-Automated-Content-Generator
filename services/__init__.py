"""
Services module - core business logic organized by feature.

Structure:
  - scraper/        : News data collection
  - scoring_engine/ : Signal analysis and scoring
  - meme_engine/    : Content generation (LLM-based)
  - post_router/    : Distribution and routing
  - writers/        : Platform-specific content writers
  - posters/        : Platform-specific posting implementations
  - infrastructure/ : Base classes and factories

Each service is independent and can be tested in isolation.
"""

# Core services
from services import scraper, scoring_engine, meme_engine, post_router, infrastructure

# Content & Distribution
from services.writers import TwitterWriter, MediumWriter, YouTubeWriter, write_twitter, write_medium, write_youtube
from services.posters import TwitterPoster, MediumPoster, YouTubePoster, post_to_twitter, post_to_medium, post_to_youtube, post_to_instagram, save_medium_draft, save_youtube_draft, post_to_platform
from services.post_router import LivePoster, post_live, build_post_payload

# Content Generation
from services.meme_engine import LLMEngine, generate_content

# Infrastructure
from services.infrastructure import BasePoster, BaseWriter, PostPayload, PosterFactory

# Scoring
from services.scoring_engine import MarketSignalScorer

# Scraping
from services.scraper import scrape_news

__all__ = [
    # Writers
    'TwitterWriter',
    'write_twitter',
    'MediumWriter',
    'write_medium',
    'YouTubeWriter',
    'write_youtube',
    
    # Posters
    'TwitterPoster',
    'post_to_twitter',
    'MediumPoster',
    'post_to_medium',
    'save_medium_draft',
    'YouTubePoster',
    'post_to_youtube',
    'save_youtube_draft',
    'post_to_instagram',
    'post_to_platform',
    
    # Posting Orchestration
    'LivePoster',
    'post_live',
    'build_post_payload',
    
    # Content Generation
    'LLMEngine',
    'generate_content',
    
    # Infrastructure
    'BasePoster',
    'BaseWriter',
    'PostPayload',
    'PosterFactory',
    
    # Scoring
    'MarketSignalScorer',
    
    # Scraping
    'scrape_news',
    
    # Services
    'scraper',
    'scoring_engine',
    'meme_engine',
    'post_router',
    'infrastructure',
]


