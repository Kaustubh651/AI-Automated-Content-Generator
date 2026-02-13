# services/meme_engine/content_generator.py

from services.meme_engine.content_refiner import ContentRefiner
from services.meme_engine.content_writer import write_twitter, write_medium, write_youtube
from shared.utils.output_writer import OutputWriter


def apply_content_bias(text: str, trend_status: str):
    if trend_status == "RISING":
        return "🔥 This topic is rapidly gaining attention.\n\n" + text
    elif trend_status == "FALLING":
        return "📉 This topic is losing momentum.\n\n" + text
    return text


def generate_content(article_text: str, platform: str, trend_status: str = "STABLE") -> str:
    """
    Central content generation entry point.
    """
    biased_text = apply_content_bias(article_text, trend_status)

    if platform == "twitter":
        raw_text = write_twitter(biased_text)

    elif platform == "medium":
        raw_text = write_medium(biased_text)

    elif platform == "youtube":
        raw_text = write_youtube(biased_text)

    else:
        raise ValueError(f"Unsupported platform: {platform}")

    refiner = ContentRefiner()
    final_text = refiner.refine(
        text=raw_text,
        style=platform
    )

    output = OutputWriter()
    saved_path = output.save(final_text, platform)
    print(f"✅ Content saved to {saved_path}")

    return final_text

