# agents/content_generator.py

from agents.content_refiner import ContentRefiner
from agents.twitter_writer import write_twitter
from agents.medium_writer import write_medium
from agents.youtube_writer import write_youtube
from utils.output_writer import save_output
from utils.output_writer import save_output


def generate_content(article_text: str, platform: str) -> str:
    """
    Central content generation entry point.
    """

    if platform == "twitter":
        raw_text = write_twitter(article_text)

    elif platform == "medium":
        raw_text = write_medium(article_text)

    elif platform == "youtube":
        raw_text = write_youtube(article_text)

    else:
        raise ValueError(f"Unsupported platform: {platform}")

    refiner = ContentRefiner()
    final_text = refiner.refine(
        text=raw_text,
        style=platform   # ✅ FIXED
    )

    saved_path = save_output(final_text, platform)
    print(f"✅ Content saved to {saved_path}")

    return final_text

