# services/scoring_engine/trend_evolution.py

import json
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path("data/memory")
TREND_MEMORY_FILE = MEMORY_DIR / "trend_memory.json"

MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _load_memory():
    if not TREND_MEMORY_FILE.exists():
        return {}
    with open(TREND_MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_memory(memory):
    with open(TREND_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)


# ==================================================
# SPRINT 4 — UPDATE MEMORY
# ==================================================
def update_trend_memory(trends):
    memory = _load_memory()
    now = datetime.utcnow().isoformat()

    for trend in trends:
        topic = trend["topic"]

        if topic not in memory:
            memory[topic] = {
                "count": 0,
                "first_seen": now,
                "last_seen": now
            }

        memory[topic]["count"] += 1
        memory[topic]["last_seen"] = now

    _save_memory(memory)


# ==================================================
# ✅ SPRINT 5 — READ ALL EVOLUTION STATES
# ==================================================
def get_trend_evolution_status():
    """
    Returns:
    {
        "openai agents": "RISING",
        "autonomous ai": "STABLE",
        ...
    }
    """
    memory = _load_memory()
    evolution_map = {}

    for topic, meta in memory.items():
        count = meta.get("count", 0)

        if count >= 5:
            status = "STABLE"
        elif count >= 2:
            status = "RISING"
        else:
            status = "NEW"

        evolution_map[topic] = status

    return evolution_map