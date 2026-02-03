from agents.content_refiner import ContentRefiner

from agents.twitter_writer import write_twitter
from agents.medium_writer import write_medium
from agents.youtube_writer import write_youtube

def generate_content(article_text, platform):
    if platform == "twitter":
        return write_twitter(article_text)
    elif platform == "medium":
        return write_medium(article_text)
    elif platform == "youtube":
        return write_youtube(article_text)
    else:
        raise ValueError("Unsupported platform")
        
