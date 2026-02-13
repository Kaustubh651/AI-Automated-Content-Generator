"""
Agents backward-compatibility exports.
This file re-exports key symbols from the new `services` and `shared` modules
so existing imports using `agents.*` continue to work during migration.
"""

# Writers (legacy names point to post_router writers)
from services.post_router.twitter_writer import TwitterWriter, write_twitter
from services.post_router.medium_writer import MediumWriter, write_medium
from services.post_router.youtube_writer import YouTubeWriter, write_youtube
from services.post_router.llm_writer import generate_simple as write_llm_content

# Posters & infrastructure
from services.infrastructure.base_poster import BasePoster, PostPayload
from services.infrastructure.poster_factory import PosterFactory
from services.post_router.twitter_poster import TwitterPoster, post_to_twitter
from services.post_router.medium_poster import MediumPoster, post_to_medium, save_medium_draft
from services.post_router.youtube_poster import YouTubePoster, post_to_youtube, save_youtube_draft
from services.instagram_poster.instagram_poster import post_to_instagram
from services.post_router.live_poster import LivePoster, post_live

# Content & LLM
from services.meme_engine.llm_engine import LLMEngine
from services.meme_engine.content_generator import generate_content
from services.meme_engine.content_refiner import ContentRefiner
from services.meme_engine.content_selector import select_top_news as ContentSelector
from services.meme_engine.content_writer import write_twitter as ContentWriter

# Data & scoring
from services.scoring_engine.market_signal_collector import collect_market_signals
from services.scoring_engine.market_signal_scorer import MarketSignalScorer
from services.scraper.news_scraper import scrape_news

# Trends
from services.scoring_engine.trend_memory import load_memory, update_memory, init_memory
from services.scoring_engine.trend_evolution import update_trend_memory as analyze_trend_evolution
from services.scoring_engine.trend_bias_engine import apply_trend_bias

# Post building
from services.post_router.post_payload_builder import build_post_payload
from services.meme_engine.image_generator import generate_instagram_image as generate_image
from services.post_router.platform_poster import post_to_platform

__all__ = [
    # Writers
    'TwitterWriter',
    'write_twitter',
    'MediumWriter',
    'write_medium',
    'YouTubeWriter',
    'write_youtube',
    'write_llm_content',

    # Posters
    'BasePoster',
    'PostPayload',
    'PosterFactory',
    'TwitterPoster',
    'post_to_twitter',
    'MediumPoster',
    'post_to_medium',
    'save_medium_draft',
    'YouTubePoster',
    'post_to_youtube',
    'save_youtube_draft',
    'post_to_instagram',
    'LivePoster',
    'post_live',

    # Content
    'LLMEngine',
    'generate_content',
    'ContentRefiner',
    'ContentSelector',
    'ContentWriter',
    'build_post_payload',
    'generate_image',
    'post_to_platform',

    # Data
    'collect_market_signals',
    'MarketSignalScorer',
    'scrape_news',

    # Trends
    'load_memory',
    'update_memory',
    'init_memory',
    'analyze_trend_evolution',
    'apply_trend_bias',
]
