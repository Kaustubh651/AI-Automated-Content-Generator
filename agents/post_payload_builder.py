# agents/post_payload_builder.py

import json
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("outputs")
QUEUE_DIR = Path("data/post_queue")
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

def build_post_payload(trend, platform):
    """
    Build a structured post payload from generated content.
    """

    file_map = {
        "twitter": "twitter.txt",
        "medium": "medium.md",
        "youtube": "youtube.txt",
        "instagram": "twitter.txt"  # reuse short-form
    }

    file_path = OUTPUT_DIR / file_map[platform]

    if not file_path.exists():
        raise FileNotFoundError(f"No content found for {platform}")

    content = file_path.read_text(encoding="utf-8")

    payload = {
        "platform": platform,
        "trend": trend,
        "content": content,
        "created_at": datetime.utcnow().isoformat(),
        "status": "READY"
    }

    out_file = QUEUE_DIR / f"{platform}_{trend.replace(' ', '_')}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"[SPRINT 6B] 📦 Payload queued → {out_file.name}")

    return payload
