import pandas as pd
from newspaper import Article
from datetime import datetime

# You can later replace this with real RSS / API sources
NEWS_URLS = [
    "https://openai.com/blog",
    "https://www.theverge.com/ai-artificial-intelligence",
]

OUTPUT_PATH = "data/raw/news_sample.csv"


def scrape_article(url: str) -> dict | None:
    """
    Scrape a single article and return structured data
    """
    try:
        article = Article(url)
        article.download()
        article.parse()

        if not article.text.strip():
            return None

        return {
            "title": article.title,
            "text": article.text,
            "url": url,
            "scraped_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        print(f"[ERROR] Failed to scrape {url}: {e}")
        return None


def scrape_news() -> pd.DataFrame:
    """
    Scrape all news sources and save to CSV
    """
    articles = []

    for url in NEWS_URLS:
        print(f"[INFO] Scraping: {url}")
        data = scrape_article(url)
        if data:
            articles.append(data)

    if not articles:
        raise RuntimeError("No articles scraped.")

    df = pd.DataFrame(articles)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"[SUCCESS] News saved to {OUTPUT_PATH}")
    return df


# Allow standalone execution
if __name__ == "__main__":
    scrape_news()
    print("News scraping completed.")
