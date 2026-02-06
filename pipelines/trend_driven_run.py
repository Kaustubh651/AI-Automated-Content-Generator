# pipelines/trend_driven_run.py

import sys
from pathlib import Path
import pandas as pd

# =========================================================
# PATH FIX — make project root importable
# =========================================================
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# =========================================================
# IMPORTS — Sprint-wise agents
# =========================================================

# Sprint 0
from agents.news_scraper import scrape_news

# Sprint 1
from agents.market_signal_collector import collect_market_signals

# Sprint 2
from agents.market_signal_scorer import MarketSignalScorer

# Sprint 3
from agents.content_generator import generate_content

# Sprint 4
from agents.trend_evolution import update_trend_memory

# Sprint 5
from agents.trend_bias_engine import apply_trend_bias

# Utils
from utils.config_loader import load_config


def main():
    print("\n" + "=" * 60)
    print("🚀 [PIPELINE START] Trend-Driven Content System")
    print("=" * 60 + "\n")

    # =====================================================
    # SPRINT 0 — NEWS SCRAPING
    # =====================================================
    print("[SPRINT 0] News Scraping → agents/news_scraper.py")
    scrape_news()
    print("[OK] News scraped successfully\n")

    # =====================================================
    # LOAD RAW NEWS
    # =====================================================
    print("[LOAD] Reading raw news articles")
    df = pd.read_csv("data/raw/news_sample.csv")

    if df.empty:
        raise ValueError("❌ No news data found. Pipeline stopped.")

    print(f"[OK] Loaded {len(df)} news articles\n")

    # =====================================================
    # SPRINT 1 — MARKET SIGNAL COLLECTION
    # =====================================================
    print("[SPRINT 1] Market Signal Collection → agents/market_signal_collector.py")
    signals = collect_market_signals(limit_per_source=5)

    if not signals:
        raise ValueError("❌ No market signals collected.")

    print(f"[OK] Collected {len(signals)} market signals\n")

    # =====================================================
    # SPRINT 2 — SIGNAL SCORING & TREND DETECTION
    # =====================================================
    print("[SPRINT 2] Trend Detection → agents/market_signal_scorer.py")
    scorer = MarketSignalScorer()
    ranked_trends = scorer.score(signals)

    if not ranked_trends:
        print("[WARN] No strong trends detected. Exiting.")
        return

    config = load_config()
    top_k = config.get("top_trends", 2)
    platforms = config.get("platforms", [])

    top_trends = ranked_trends[:top_k]

    print("\n🔥 Raw Detected Trends:")
    for t in top_trends:
        print(f"  • {t['topic']} (score={round(t['score'], 3)})")

    # =====================================================
    # SPRINT 4 — TREND MEMORY UPDATE (LEARNING INPUT)
    # =====================================================
    print("\n[SPRINT 4] Updating Trend Memory → agents/trend_evolution.py")
    update_trend_memory(top_trends)
    print("[OK] Trend memory updated\n")

    # =====================================================
    # SPRINT 5 — APPLY LEARNING / BIAS ENGINE
    # =====================================================
    print("[SPRINT 5] Applying Learning Bias → agents/trend_bias_engine.py")
    biased_trends = apply_trend_bias(top_trends)

    print("\n🔥 Final Trends After Learning:")
    for t in biased_trends:
        bias = t.get("bias_status", "NEUTRAL")
        print(f"  • {t['topic']} (score={round(t['score'], 3)}, bias={bias})")

    # =====================================================
    # SPRINT 3 — CONTENT GENERATION (PLATFORM-WISE)
    # =====================================================
    print("\n[SPRINT 3] Content Generation → agents/content_generator.py")

    for trend in biased_trends:
        print(f"\n[GEN] Trend: {trend['topic']}")

        related_articles = [
            s["summary"]
            for s in signals
            if trend["topic"].lower() in s["title"].lower()
        ]

        article_text = " ".join(related_articles)

        if not article_text.strip():
            print("  ⚠️ No related content found, skipping")
            continue

        for platform in platforms:
            print(f"  → Generating for {platform.upper()}")
            generate_content(
                article_text,
                platform,
                trend_status=trend["bias_status"]
            )

    print("\n" + "=" * 60)
    print("✅ [PIPELINE COMPLETE] Content generated for all platforms")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
