# utils/output_writer.py

import os
from datetime import datetime


OUTPUT_DIR = "outputs"


def save_output(content: str, platform: str) -> str:
    """
    Save generated content to disk by platform.
    Returns saved file path.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ext = {
        "twitter": "txt",
        "medium": "md",
        "youtube": "txt"
    }.get(platform, "txt")

    filename = f"{platform}.{ext}"
    path = os.path.join(OUTPUT_DIR, filename)

    header = f"Generated on: {datetime.now()}\nPlatform: {platform.upper()}\n\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(content.strip())

    return path
