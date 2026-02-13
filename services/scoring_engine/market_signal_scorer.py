# services/scoring_engine/market_signal_scorer.py

import math
from datetime import datetime
from collections import defaultdict


TREND_KEYWORDS = [
    "ai", "agent", "autonomous", "openai", "launch",
    "release", "framework", "model", "regulation",
    "startup", "funding", "policy"
]


class MarketSignalScorer:
    def __init__(self, decay_hours=48):
        self.decay_hours = decay_hours

    # ---------- PUBLIC ----------
    def score(self, signals):
        """
        signals: list of dicts
        Each dict must contain: title, summary, source, timestamp
        """

        grouped = self._group_by_topic(signals)
        scored_topics = []

        for topic, items in grouped.items():
            score = self._compute_score(items)
            scored_topics.append({
                "topic": topic,
                "score": round(score, 3),
                "mentions": len(items),
                "sources": list(set(i["source"] for i in items))
            })

        scored_topics.sort(key=lambda x: x["score"], reverse=True)
        return scored_topics

    # ---------- CORE LOGIC ----------
    def _compute_score(self, items):
        freq_score = math.log(len(items) + 1)

        recency_score = sum(
            self._recency_weight(i["timestamp"]) for i in items
        ) / len(items)

        keyword_score = sum(
            self._keyword_strength(i["title"] + " " + i["summary"])
            for i in items
        ) / len(items)

        source_diversity = len(set(i["source"] for i in items))

        final_score = (
            0.4 * freq_score +
            0.3 * recency_score +
            0.2 * keyword_score +
            0.1 * source_diversity
        )

        return final_score

    # ---------- HELPERS ----------
    def _recency_weight(self, timestamp):
        """
        Expects ISO timestamp string
        """
        now = datetime.utcnow()
        t = datetime.fromisoformat(timestamp)
        hours_diff = (now - t).total_seconds() / 3600

        return math.exp(-hours_diff / self.decay_hours)

    def _keyword_strength(self, text):
        text = text.lower()
        hits = sum(1 for kw in TREND_KEYWORDS if kw in text)
        return hits / max(len(TREND_KEYWORDS), 1)

    def _group_by_topic(self, signals):
        buckets = defaultdict(list)

        for s in signals:
            topic = self._extract_topic(s["title"])
            buckets[topic].append(s)

        return buckets

    def _extract_topic(self, title):
        """
        Naive topic extraction (will improve in Sprint 4)
        """
        words = title.split()
        return " ".join(words[:4]).lower()
