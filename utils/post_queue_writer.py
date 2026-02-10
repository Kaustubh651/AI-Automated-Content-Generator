import json
from pathlib import Path
from datetime import datetime

POST_QUEUE_DIR = Path("data/post_queue")
POST_QUEUE_DIR.mkdir(parents=True, exist_ok=True)


def queue_post(platform: str, topic: str, content: str):
    payload = {
        "platform": platform.upper(),
        "topic": topic,
        "content": content,
        "queued_at": datetime.utcnow().isoformat()
    }

    filename = f"{platform.lower()}_{int(datetime.utcnow().timestamp())}.json"
    path = POST_QUEUE_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"[QUEUE] 📥 Added post → {path}")
