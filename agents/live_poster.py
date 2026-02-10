import sys
from pathlib import Path
import pandas as pd

# =========================================================
# PATH FIX
# =========================================================
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
import json
from pathlib import Path
from datetime import datetime
from agents.twitter_poster import post_to_twitter
# from agents.medium_poster import post_to_medium
from agents.youtube_poster import post_to_youtube
from agents.instagram_poster import post_to_instagram
# =========================================
# CONFIG
# =========================================
POST_QUEUE_DIR = Path("data/post_queue")
ALLOWED_PLATFORMS = {"TWITTER", "MEDIUM"}
LIVE_MODE = True  # 🔴 REAL POSTING SWITCH


def post_live():
    print("\n[SPRINT 6C] 🚀 Live Posting Engine Started\n")

    if not POST_QUEUE_DIR.exists():
        print("[ERROR] No post queue found")
        return

    for payload_file in POST_QUEUE_DIR.glob("*.json"):
        with open(payload_file, "r", encoding="utf-8") as f:
            payload = json.load(f)

        platform = payload.get("platform", "").upper()
        topic = payload.get("topic", "UNKNOWN")

        if platform not in ALLOWED_PLATFORMS:
            print(f"[SKIP] {platform} not enabled for live posting")
            continue

        print(f"\n[POST] Platform: {platform}")
        print(f"Topic: {topic}")

        if not LIVE_MODE:
            print("[SAFE MODE] Live posting disabled")
            continue

        # ===============================
        # REAL POSTING PLACEHOLDER
        # ===============================
        # Twitter API → next step
        # Medium API  → next step

        print(f"[LIVE] ✅ Posted to {platform} at {datetime.utcnow()}")
        
        if platform == "TWITTER":
            try:
                post_to_twitter(payload["content"])
            except Exception as e:
                print(f"[ERROR] Twitter posting failed: {e}")
                continue
        # if platform == "MEDIUM":
        #     post_to_medium(
        #         title=payload.get("topic", "Automated Insight"),
        #         content=payload["content"]
        #     )

        elif platform == "TWITTER":
            post_to_twitter(payload["content"])

        elif platform == "YOUTUBE":
            post_to_youtube(payload["content"])

        elif platform == "INSTAGRAM":
            post_to_instagram(payload["content"])

    print("\n[SPRINT 6C] ✅ Live posting cycle complete\n")


if __name__ == "__main__":
    post_live()
