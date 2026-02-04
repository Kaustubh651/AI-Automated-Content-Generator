# pipelines/trend_driven_run.py

import sys
from pathlib import Path
import pandas as pd

# -------- PATH FIX --------
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# -------- IMPORTS --------
from agents.news_scraper import scrape_news
from agents.market_signal_collector import collect_market_signals
from agents.market_signal_scorer import MarketSignalScorer
from agents.content_generator import generate_content
from utils.config_loader import load_config


def main():
    print("\n[START] Trend-driven content pipeline\n")

    # 1. Load config
    config = load_config()
    platforms = config["platforms"]
    top_k = config.get("top_trends", 2)

    # 2. Scrape news
    scrape_news()
    print("[OK] News scraped")

    # 3. Load raw articles
    df = pd.read_csv("data/raw/news_sample.csv")
    if df.empty:
        raise ValueError("No news data found")

    # 4. Collect market signals
    signals = collect_market_signals(limit_per_source=5)

    print(f"[OK] Collected {len(signals)} market signals")

    # 5. Score trends
    scorer = MarketSignalScorer()
    ranked_trends = scorer.score(signals)

    if not ranked_trends:
        print("[WARN] No strong trends detected")
        return

    top_trends = ranked_trends[:top_k]
    print("\n🔥 Top Market Trends:")
    for t in top_trends:
        print(f"- {t['topic']} (score: {t['score']})")

    # 6. Generate content per trend
    for trend in top_trends:
        print(f"\n[GEN] Generating content for trend: {trend['topic']}")

        related_articles = [
            s["summary"] for s in signals if trend["topic"] in s["title"].lower()
        ]

        article_text = " ".join(related_articles)

        for platform in platforms:
            print(f"  → {platform.upper()}")
            generate_content(article_text, platform)

    print("\n[SUCCESS] Trend-driven content generation complete\n")


if __name__ == "__main__":
    main()
