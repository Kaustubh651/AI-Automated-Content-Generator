"""
Post routing and distribution service.
Routes content to appropriate platforms and handles cross-platform posting.
"""

from services.post_router.live_poster import LivePoster, post_live
from services.post_router.post_payload_builder import build_post_payload
from services.writers.twitter_writer import TwitterWriter, write_twitter
from services.writers.medium_writer import MediumWriter, write_medium
from services.writers.youtube_writer import YouTubeWriter, write_youtube
from services.posters.twitter_poster import TwitterPoster, post_to_twitter
from services.posters.medium_poster import MediumPoster, post_to_medium, save_medium_draft
from services.posters.youtube_poster import YouTubePoster, post_to_youtube, save_youtube_draft
from services.posters.platform_poster import post_to_platform

__all__ = [
    'LivePoster',
    'post_live',
    'build_post_payload',
    'post_to_platform',
    'TwitterWriter',
    'write_twitter',
    'MediumWriter',
    'write_medium',
    'YouTubeWriter',
    'write_youtube',
    'TwitterPoster',
    'post_to_twitter',
    'MediumPoster',
    'post_to_medium',
    'save_medium_draft',
    'YouTubePoster',
    'post_to_youtube',
    'save_youtube_draft',
]

