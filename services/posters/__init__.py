"""
Posters Service
Contains all poster implementations that handle platform-specific API interactions.
"""

from services.infrastructure.base_poster import BasePoster, PostPayload
from services.infrastructure.poster_factory import PosterFactory
from services.posters.twitter_poster import TwitterPoster, post_to_twitter
from services.posters.medium_poster import MediumPoster, post_to_medium, save_medium_draft
from services.posters.youtube_poster import YouTubePoster, post_to_youtube, save_youtube_draft
from services.posters.instagram_poster import post_to_instagram
from services.posters.platform_poster import post_to_platform

__all__ = [
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
    'InstagramPoster',
    'post_to_instagram',
]
