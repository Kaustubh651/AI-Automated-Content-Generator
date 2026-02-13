"""
Live Posting Engine.
Orchestrates posting to all platforms using factory pattern.
Single Responsibility: Process queue and route to appropriate poster.
Configuration-driven: No hard-coded platform lists or modes.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# PATH FIX
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from agents.poster_factory import PosterFactory
from agents.base_poster import PostPayload
from utils.config_loader import ConfigLoader


class LivePoster:
    """
    Main posting orchestrator.
    Dependency Injection: Config, queue dir, enabled platforms all injected.
    """
    
    def __init__(
        self,
        queue_dir: Path = None,
        enabled_platforms: List[str] = None,
        live_mode: bool = None,
        logger=None
    ):
        """
        Args:
            queue_dir: Directory with post payloads. If None, uses config.
            enabled_platforms: List of enabled platforms. If None, uses config.
            live_mode: Whether to actually post. If None, uses config.
            logger: Optional logger instance
        """
        self.config_loader = ConfigLoader()
        self.logger = logger
        
        # Load from config if not provided
        self.queue_dir = Path(queue_dir or self.config_loader.get("posting.queue_dir", "data/post_queue"))
        self.enabled_platforms = (
            enabled_platforms or
            self.config_loader.get("posting.enabled_platforms", ["twitter"])
        )
        self.live_mode = (
            live_mode if live_mode is not None else
            self.config_loader.is_live_mode()
        )
        
        self.results = []
    
    def post_all(self) -> Dict[str, Any]:
        """
        Process all payloads in queue and post.
        
        Returns:
            Summary dict with status and results
        """
        self._log("🚀 Live Posting Engine Started", "INFO")
        
        if not self.queue_dir.exists():
            self._log(f"Queue directory not found: {self.queue_dir}", "ERROR")
            return {"status": "error", "message": "Queue directory not found"}
        
        payload_files = list(self.queue_dir.glob("*.json"))
        
        if not payload_files:
            self._log("No payloads in queue", "WARN")
            return {"status": "empty", "message": "No payloads found"}
        
        self._log(f"Found {len(payload_files)} payloads to process", "INFO")
        
        for payload_file in payload_files:
            self._process_payload(payload_file)
        
        return self._get_summary()
    
    def _process_payload(self, payload_file: Path):
        """
        Process a single payload file.
        
        Args:
            payload_file: Path to JSON payload file
        """
        try:
            with open(payload_file, "r", encoding="utf-8") as f:
                payload_data = json.load(f)
            
            platform = payload_data.get("platform", "").lower()
            
            # Validate platform
            if not platform:
                self._log(f"Payload missing platform field: {payload_file.name}", "WARN")
                return
            
            if platform not in self.enabled_platforms:
                self._log(
                    f"Platform '{platform}' not enabled. Enabled: {self.enabled_platforms}",
                    "SKIP"
                )
                return
            
            self._log(f"Processing {platform}: {payload_data.get('title', 'Untitled')}", "INFO")
            
            # Check live mode
            if not self.live_mode:
                self._log(f"SAFE MODE: Not actually posting to {platform}", "WARN")
                self.results.append({
                    "platform": platform,
                    "status": "preview",
                    "title": payload_data.get("title"),
                    "timestamp": datetime.utcnow().isoformat()
                })
                return
            
            # Post via factory
            result = self._post_payload(payload_data)
            self.results.append(result)
            
        except json.JSONDecodeError as e:
            self._log(f"Invalid JSON in {payload_file.name}: {e}", "ERROR")
        except Exception as e:
            self._log(f"Error processing {payload_file.name}: {e}", "ERROR")
    
    def _post_payload(self, payload_data: Dict) -> Dict[str, Any]:
        """
        Post a single payload using appropriate poster.
        Uses factory pattern for loose coupling.
        
        Args:
            payload_data: Dict with payload fields
            
        Returns:
            Result dict
        """
        platform = payload_data.get("platform", "").lower()
        
        try:
            # Get poster from factory
            poster = PosterFactory.create(platform, logger=self.logger)
            
            # Build standardized payload
            payload = PostPayload(
                platform=platform,
                title=payload_data.get("title", "Automated Post"),
                content=payload_data.get("content", ""),
                tags=payload_data.get("tags", []),
                metadata=payload_data.get("metadata", {})
            )
            
            # Post
            result = poster.post(payload)
            
            # Add context
            result["title"] = payload.title
            result["timestamp"] = datetime.utcnow().isoformat()
            
            self._log(f"✅ Posted to {platform}: {result.get('status')}", "INFO")
            
            return result
            
        except ValueError as e:
            # Platform not registered
            self._log(f"Unknown platform '{platform}': {e}", "ERROR")
            return {
                "platform": platform,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            self._log(f"Posting error: {e}", "ERROR")
            return {
                "platform": platform,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _get_summary(self) -> Dict[str, Any]:
        """Get summary of posting results."""
        success_count = sum(1 for r in self.results if r.get("status") == "success")
        error_count = sum(1 for r in self.results if r.get("status") == "error")
        
        summary = {
            "status": "complete",
            "total": len(self.results),
            "success": success_count,
            "error": error_count,
            "preview": sum(1 for r in self.results if r.get("status") == "preview"),
            "results": self.results
        }
        
        # Print summary
        self._print_summary(summary)
        
        return summary
    
    def _print_summary(self, summary: Dict):
        """Pretty-print results summary."""
        print("\n" + "="*60)
        print(f"[SUMMARY] Posting Complete")
        print("="*60)
        print(f"Total: {summary['total']} | "
              f"Success: {summary['success']} | "
              f"Error: {summary['error']} | "
              f"Preview: {summary['preview']}")
        
        for result in self.results:
            status_icon = {
                "success": "✅",
                "error": "❌",
                "preview": "👁️",
                "draft": "📝"
            }.get(result.get("status"), "❓")
            
            platform = result.get("platform", "UNKNOWN").upper()
            title = result.get("title", "")[:40]
            print(f"{status_icon} {platform}: {title}")
        
        print("="*60 + "\n")
    
    def _log(self, message: str, level: str = "INFO"):
        """Helper for logging."""
        if self.logger:
            getattr(self.logger, level.lower())(message)
        else:
            prefix = f"[LIVE POSTER] [{level}]"
            print(f"{prefix} {message}")


def post_live():
    """Convenience function: create poster and post all."""
    poster = LivePoster()
    return poster.post_all()


if __name__ == "__main__":
    post_live()

