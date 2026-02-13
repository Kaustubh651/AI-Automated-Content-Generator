"""Twitter poster. Handles posting to Twitter/X via API."""

import os
import tweepy
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

from services.infrastructure.base_poster import BasePoster, PostPayload


# Load secrets once at module level
load_dotenv("config/secrets.env")


class TwitterPoster(BasePoster):
    """
    Posts content to Twitter/X.
    Encapsulates all Twitter-specific API logic.
    """
    
    def _validate_config(self):
        """Ensure required Twitter config is present."""
        # Credentials come from environment variables
        required_env = [
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET",
            "TWITTER_ACCESS_TOKEN",
            "TWITTER_ACCESS_SECRET"
        ]
        
        missing = [var for var in required_env if not os.getenv(var)]
        if missing:
            raise EnvironmentError(f"Missing Twitter credentials: {missing}")
    
    def post(self, payload: PostPayload) -> Dict[str, Any]:
        """
        Post tweet to Twitter.
        
        Args:
            payload: PostPayload with content
            
        Returns:
            {
                "status": "success" | "error",
                "url": tweet_url,
                "tweet_id": id,
                "timestamp": datetime
            }
        """
        return self._safe_post(self._post_tweet, payload.content)
    
    def _post_tweet(self, content: str) -> Dict[str, Any]:
        """
        Internal method: actually posts the tweet.
        Separated for clean error handling in _safe_post().
        
        Args:
            content: Tweet content
            
        Returns:
            Dict with tweet_id and url
        """
        # Truncate to Twitter limit
        text = content[:280]
        
        # Get credentials from environment
        api_key = os.getenv("TWITTER_API_KEY")
        api_secret = os.getenv("TWITTER_API_SECRET")
        access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        
        # Authenticate
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        # Post tweet
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        url = f"https://x.com/i/web/status/{tweet_id}"
        
        self._log(f"Tweet posted successfully: {url}")
        
        return {
            "url": url,
            "tweet_id": tweet_id,
            "timestamp": datetime.utcnow().isoformat()
        }


# Backward compatibility: standalone function
def post_to_twitter(text: str):
    """
    Legacy interface for posting to Twitter.
    Creates poster with config injection and posts.
    """
    from shared.config import get_config
    
    config = get_config().get_platform_config("twitter")
    poster = TwitterPoster(config=config)
    
    payload = PostPayload(
        platform="twitter",
        title="",
        content=text
    )
    
    result = poster.post(payload)
    
    if result["status"] == "success":
        print(f"[TWITTER] ✅ Posted: {result['url']}")
    else:
        print(f"[TWITTER] ❌ Error: {result.get('error')}")
    
    return result

