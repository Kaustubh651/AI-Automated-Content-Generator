"""YouTube poster. Handles saving scripts and optional API upload."""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import os
from dotenv import load_dotenv

from services.infrastructure.base_poster import BasePoster, PostPayload


load_dotenv("config/secrets.env")


class YouTubePoster(BasePoster):
    """
    Posts videos to YouTube.
    Currently saves scripts as drafts (full API requires video file).
    """
    
    def _validate_config(self):
        """Validate YouTube configuration."""
        # YouTube credentials are optional (in draft mode)
        pass
    
    def post(self, payload: PostPayload) -> Dict[str, Any]:
        """
        Save YouTube video script.
        
        Args:
            payload: PostPayload with title and content (script)
            
        Returns:
            Status dict with draft path
        """
        return self._save_script_draft(
            payload.title,
            payload.content,
            payload.metadata or {}
        )
    
    def _save_script_draft(
        self,
        title: str,
        script: str,
        metadata: Dict = None
    ) -> Dict[str, Any]:
        """
        Save video script as draft for manual upload.
        
        Args:
            title: Video title
            script: Video script content
            metadata: Optional metadata (tags, description, etc.)
            
        Returns:
            Dict with draft file path
        """
        from shared.config import get_config
        
        draft_dir = Path(get_config().get("posting.draft_dir", "data/drafts"))
        draft_dir.mkdir(parents=True, exist_ok=True)
        
        if metadata is None:
            metadata = {}
        
        draft = {
            "platform": "youtube",
            "title": title,
            "script": script,
            "description": metadata.get("description", f"Video about {title}"),
            "tags": metadata.get("tags", ["technology", "ai", "automation"]),
            "saved_at": datetime.utcnow().isoformat(),
            "status": "DRAFT",
            "instructions": [
                "1. Record this script as a video",
                "2. Use the title and description provided",
                "3. Add tags for discoverability",
                "4. Upload to YouTube Studio with status='unlisted' for review"
            ]
        }
        
        filename = f"youtube_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = draft_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(draft, f, indent=2)
        
        self._log(f"Script draft saved: {filepath}")
        
        return {
            "status": "draft",
            "draft_path": str(filepath),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def upload_video(self, video_path: str, title: str, description: str, tags: list):
        """
        Upload video via YouTube API.
        Requires video file and credentials.
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            
        Returns:
            Upload result dict
        """
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
        except ImportError:
            raise ImportError("google-auth and google-api-python-client required for upload")
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # This would require proper OAuth setup
        # For now, this is a placeholder
        self._log("Full video upload requires proper OAuth setup", "WARN")
        return {
            "status": "not_implemented",
            "message": "Please configure YouTube OAuth for full upload"
        }


# Backward compatibility
def post_to_youtube(content: str):
    """Legacy interface for YouTube posting."""
    from shared.config import get_config
    
    config = get_config().get_platform_config("youtube")
    poster = YouTubePoster(config=config)
    
    payload = PostPayload(
        platform="youtube",
        title="Automated Video",
        content=content
    )
    
    return poster.post(payload)


def save_youtube_draft(title: str, script: str, description: str = None):
    """Legacy interface for saving YouTube draft."""
    config = {}
    poster = YouTubePoster(config=config)
    
    metadata = {}
    if description:
        metadata["description"] = description
    
    return poster._save_script_draft(title, script, metadata)

