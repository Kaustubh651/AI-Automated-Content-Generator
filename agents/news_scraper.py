from newspaper import Article
import pandas as pd

def scrape_news():
    # your scraping logic here
    # example:
    data = [
        {"title": "AI news", "text": "OpenAI released a framework", "url": "https://example.com"}
    ]
    df = pd.DataFrame(data)
    df.to_csv("data/raw/news_sample.csv", index=False)
    print("News saved to data/raw/news_sample.csv")
    return df

# if script is run directly
if __name__ == "__main__":
    scrape_news()
    print("News scraping completed.")
