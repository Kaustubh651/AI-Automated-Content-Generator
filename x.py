# Example script: run_pipeline.py
from agents.news_scraper import scrape_news
from agents.content_selector import select_top_news
from agents.content_generator import generate_content
import pandas as pd

# 1. Scrape news
scrape_news()

# 2. Load and select top news
df = pd.read_csv("data/raw/news_sample.csv")
top_article = select_top_news(df, top_n=1)

# 3. Generate and refine content
for platform in ["twitter", "medium", "youtube"]:
    content = generate_content(top_article['text'].values[0], platform)
    print(f"\n=== {platform.upper()} ===\n")
    print(content)
