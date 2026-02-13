"""Medium poster. Handles posting to Medium via API or drafts."""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

from services.infrastructure.base_poster import BasePoster, PostPayload


load_dotenv("config/secrets.env")


class MediumPoster(BasePoster):
    """
    Posts articles to Medium.
    Falls back to local draft if API unavailable.
    """
    
    def _validate_config(self):
        """Validate Medium configuration."""
        # Medium API is optional - can fallback to draft saving
        pass
    
    def post(self, payload: PostPayload) -> Dict[str, Any]:
        """
        Post article to Medium.
        
        Args:
            payload: PostPayload with title and content
            
        Returns:
            Status dict with url or draft path
        """
        # Try API first, fallback to draft
        api_token = os.getenv("MEDIUM_API_TOKEN")
        
        if api_token:
            return self._safe_post(
                self._post_to_api,
                payload.title,
                payload.content,
                payload.tags or []
            )
        else:
            self._log("No API token, saving as draft", "WARN")
            return self._save_draft(payload.title, payload.content)
    
    def _post_to_api(self, title: str, content: str, tags: list) -> Dict[str, Any]:
        """
        Internal: Post via Medium API.
        
        Args:
            title: Article title
            content: Article content (markdown)
            tags: Article tags
            
        Returns:
            Dict with article_url
        """
        try:
            import requests
        except ImportError:
            raise ImportError("requests library required for Medium API")
        
        api_token = os.getenv("MEDIUM_API_TOKEN")
        headers = {"Authorization": f"Bearer {api_token}"}
        
        # Get user ID
        user_resp = requests.get("https://api.medium.com/v1/me", headers=headers)
        user_resp.raise_for_status()
        user_id = user_resp.json()["data"]["id"]
        
        # Create post
        post_data = {
            "title": title,
            "contentFormat": "markdown",
            "content": content,
            "publishStatus": "draft",
            "tags": tags[:5]
        }
        
        post_resp = requests.post(
            f"https://api.medium.com/v1/users/{user_id}/posts",
            headers=headers,
            json=post_data
        )
        post_resp.raise_for_status()
        
        url = post_resp.json()["data"]["url"]
        self._log(f"Article posted: {url}")
        
        return {
            "url": url,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _save_draft(self, title: str, content: str) -> Dict[str, Any]:
        """
        Fallback: Save article as local draft.
        
        Args:
            title: Article title
            content: Article content
            
        Returns:
            Dict with draft file path
        """
        from shared.config import get_config
        
        draft_dir = Path(get_config().get("posting.draft_dir", "data/drafts"))
        draft_dir.mkdir(parents=True, exist_ok=True)
        
        draft = {
            "platform": "medium",
            "title": title,
            "content": content,
            "saved_at": datetime.utcnow().isoformat(),
            "status": "DRAFT"
        }
        
        filename = f"medium_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = draft_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(draft, f, indent=2)
        
        self._log(f"Draft saved: {filepath}")
        
        return {
            "status": "draft",
            "draft_path": str(filepath),
            "timestamp": datetime.utcnow().isoformat()
        }


# Backward compatibility
def post_to_medium(article_title: str, article_content: str, tags: list = None):
    """Legacy interface for Medium posting."""
    from shared.config import get_config
    
    config = get_config().get_platform_config("medium")
    poster = MediumPoster(config=config)
    
    payload = PostPayload(
        platform="medium",
        title=article_title,
        content=article_content,
        tags=tags or []
    )
    
    return poster.post(payload)


def save_medium_draft(article_title: str, article_content: str):
    """Legacy interface for saving draft."""
    config = {}
    poster = MediumPoster(config=config)
    return poster._save_draft(article_title, article_content)

