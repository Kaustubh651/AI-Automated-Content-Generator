import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from agents.market_signal_scorer import MarketSignalScorer

signals = [
    {
        "title": "OpenAI launches autonomous AI agents",
        "summary": "New framework enables task execution",
        "source": "theverge",
        "timestamp": "2026-01-30T10:00:00"
    },
    {
        "title": "Autonomous AI agents are the future",
        "summary": "Industry reacts",
        "source": "openai_blog",
        "timestamp": "2026-01-30T12:00:00"
    }
]

scorer = MarketSignalScorer()
print(scorer.score(signals))
