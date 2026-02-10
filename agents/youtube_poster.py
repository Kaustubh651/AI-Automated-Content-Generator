from pathlib import Path
from datetime import datetime

def post_to_youtube(content):
    output = Path("outputs/youtube_ready.txt")

    with open(output, "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.utcnow()} ---\n")
        f.write(content)

    print("🟡 YouTube content prepared (manual upload)")
