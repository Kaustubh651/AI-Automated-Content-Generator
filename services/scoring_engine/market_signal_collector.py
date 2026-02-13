# services/scoring_engine/market_signal_collector.py

import csv
from datetime import datetime
from pathlib import Path

import feedparser


# ---------------- CONFIG ----------------
RSS_SOURCES = {
    "ai_news": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "tech_news": "https://www.theverge.com/rss/index.xml"
}

OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "market_signals.csv"


# ---------------- CORE ----------------
def collect_market_signals(limit_per_source: int = 5):
    """
    Collects raw market signals from public RSS feeds
    and stores them in a structured CSV.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    signals = []

    for source_name, feed_url in RSS_SOURCES.items():
        print(f"[SIGNAL] Fetching from {source_name}")

        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:limit_per_source]:
            signal = {
                "timestamp": datetime.utcnow().isoformat(),
                "source": source_name,
                "title": entry.get("title", "").strip(),
                "summary": entry.get("summary", "").strip(),
                "link": entry.get("link", ""),
                "type": "news"
            }
            signals.append(signal)

    _save_signals(signals)
    print(f"[OK] {len(signals)} market signals collected")
    return signals


# ---------------- SAVE ----------------
def _save_signals(signals):
    if not signals:
        print("[WARN] No signals to save")
        return

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=signals[0].keys()
        )
        writer.writeheader()
        writer.writerows(signals)

    print(f"[SAVE] Signals written to {OUTPUT_FILE}")


# ---------------- CLI TEST ----------------
if __name__ == "__main__":
    collect_market_signals()
