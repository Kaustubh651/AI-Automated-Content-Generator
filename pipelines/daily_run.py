# run.py
import sys
from pathlib import Path
import pandas as pd

# ---------------- PATH FIX ----------------
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))


# ---------------- IMPORTS ----------------
from services.scraper import scrape_news
from services.meme_engine import generate_content
from shared.config import get_config

def load_config():
    # Backwards-compatible wrapper
    return get_config().get_all()


def main():
    print("[START] Running content automation pipeline\n")

    # 1. Load config
    config = load_config()
    platforms = config["platforms"]

    # 2. Scrape news
    scrape_news()
    print("[OK] News scraped")

    # 3. Load article
    df = pd.read_csv("data/raw/news_sample.csv")

    if df.empty:
        raise ValueError("No news articles found")

    article_text = df.iloc[0]["text"]
    print("[OK] Article loaded\n")

    # 4. Generate content
    for platform in platforms:
        print(f"[GEN] Generating content for {platform.upper()}")
        output = generate_content(article_text, platform)
        print(output)
        print("-" * 60)

    print("\n[SUCCESS] All content generated successfully")


if __name__ == "__main__":
    main()
