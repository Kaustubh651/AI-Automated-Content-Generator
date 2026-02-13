# shared/utils/output_writer.py

import os
from datetime import datetime


class OutputWriter:
    """Utility for saving generated content to disk."""
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize output writer with directory."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save(self, content: str, platform: str) -> str:
        """
        Save generated content to disk by platform.
        Returns saved file path.
        """
        ext = {
            "twitter": "txt",
            "medium": "md",
            "youtube": "txt",
            "instagram": "txt"
        }.get(platform, "txt")

        filename = f"{platform}.{ext}"
        path = os.path.join(self.output_dir, filename)

        header = f"Generated on: {datetime.now()}\nPlatform: {platform.upper()}\n\n"

        with open(path, "w", encoding="utf-8") as f:
            f.write(header)
            f.write(content.strip())

        return path


# Convenience function for backward compatibility
def save_output(content: str, platform: str) -> str:
    """Save generated content to disk by platform."""
    writer = OutputWriter()
    return writer.save(content, platform)
