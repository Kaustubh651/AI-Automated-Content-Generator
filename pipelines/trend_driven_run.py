import sys
from pathlib import Path
import pandas as pd

# =========================================================
# PATH FIX
# =========================================================
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# =========================================================
# IMPORTS
# =========================================================

# Sprint 0
from services.scraper import scrape_news

# Sprint 1
from services.scoring_engine import collect_market_signals

# Sprint 2
from services.scoring_engine import MarketSignalScorer

# Sprint 3
from services.meme_engine import generate_content

# Sprint 4
from services.scoring_engine import update_trend_memory

# Sprint 5
from services.scoring_engine import apply_trend_bias

# Sprint 6B
from services.post_router import build_post_payload, post_to_platform

# Utils
from shared.config import get_config

def load_config():
    return get_config().get_all()

def main():
    print("\n" + "=" * 60)
    print("🚀 [PIPELINE START] Trend-Driven Content System")
    print("=" * 60 + "\n")

    # =====================================================
    # SPRINT 0 — NEWS SCRAPING
    # =====================================================
    print("[SPRINT 0] News Scraping")
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
    print("[SPRINT 1] Market Signal Collection")
    signals = collect_market_signals(limit_per_source=5)

    if not signals:
        raise ValueError("❌ No market signals collected.")

    print(f"[OK] Collected {len(signals)} market signals\n")

    # =====================================================
    # SPRINT 2 — TREND DETECTION
    # =====================================================
    print("[SPRINT 2] Trend Detection")
    scorer = MarketSignalScorer()
    ranked_trends = scorer.score(signals)

    if not ranked_trends:
        print("[WARN] No strong trends detected.")
        return

    config = load_config()
    platforms = config.get("platforms", [])
    top_k = config.get("top_trends", 2)

    top_trends = ranked_trends[:top_k]

    print("\n🔥 Raw Detected Trends:")
    for t in top_trends:
        print(f"  • {t['topic']} (score={round(t['score'], 3)})")

    # =====================================================
    # SPRINT 4 — TREND MEMORY UPDATE
    # =====================================================
    print("\n[SPRINT 4] Updating Trend Memory")
    update_trend_memory(top_trends)
    print("[OK] Trend memory updated\n")

    # =====================================================
    # SPRINT 5 — LEARNING / BIAS ENGINE
    # =====================================================
    print("[SPRINT 5] Applying Learning Bias")
    biased_trends = apply_trend_bias(top_trends)

    print("\n🔥 Final Trends After Learning:")
    for t in biased_trends:
        print(
            f"  • {t['topic']} "
            f"(score={round(t['score'], 3)}, bias={t['bias_status']})"
        )

    # =====================================================
    # SPRINT 3 — CONTENT GENERATION
    # =====================================================
    print("\n[SPRINT 3] Content Generation")

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

    # =====================================================
    # SPRINT 6B — POST PREPARATION (SAFE MODE)
    # =====================================================
    print("\n[SPRINT 3 → 6B] Content Generation & Post Queueing")

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
            print(f"  → Generating & queueing for {platform.upper()}")

            content = generate_content(
                article_text,
                platform,
                trend_status=trend["bias_status"]
            )

            # Build and queue post payload
            build_post_payload(
                trend=trend["topic"],
                platform=platform
            )


if __name__ == "__main__":
    main()
