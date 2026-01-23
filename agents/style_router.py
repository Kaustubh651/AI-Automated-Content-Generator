from agents.content_refiner import ContentRefiner
from agents.twitter_writer import write_twitter
from agents.medium_writer import write_medium
from agents.youtube_writer import write_youtube

def generate_content(article_text, platform):
    # Generate raw content first
    if platform == "twitter":
        generated_text = write_twitter(article_text)
    elif platform == "medium":
        generated_text = write_medium(article_text)
    elif platform == "youtube":
        generated_text = write_youtube(article_text)
    else:
        raise ValueError("Unsupported platform")
    
    # Refine content before returning
    refiner = ContentRefiner()
    final_output = refiner.refine(
        text=generated_text,
        style=platform  # twitter / medium / youtube
    )

    return final_output
