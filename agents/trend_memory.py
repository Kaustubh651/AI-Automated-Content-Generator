# agents/trend_memory.py

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# ---------------- PATHS ----------------
MEMORY_DIR = Path("data/memory")
MEMORY_FILE = MEMORY_DIR / "trend_memory.csv"

FIELDS = [
    "trend",
    "first_seen",
    "last_seen",
    "frequency",
    "avg_score"
]


# ---------------- INIT ----------------
def init_memory():
    """
    Initialize memory storage if not present.
    """
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    if not MEMORY_FILE.exists():
        with open(MEMORY_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


# ---------------- LOAD ----------------
def load_memory() -> Dict[str, Dict]:
    """
    Load memory into dict keyed by trend.
    """
    init_memory()
    memory = {}

    with open(MEMORY_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            memory[row["trend"]] = {
                "first_seen": row["first_seen"],
                "last_seen": row["last_seen"],
                "frequency": int(row["frequency"]),
                "avg_score": float(row["avg_score"])
            }

    return memory


# ---------------- UPDATE ----------------
def update_memory(trends: List[Dict]):
    """
    Update memory using newly detected trends.
    trends = [{"trend": str, "score": float}]
    """
    memory = load_memory()
    now = datetime.utcnow().isoformat()

    for item in trends:
        trend = item["trend"].lower().strip()
        score = float(item["score"])

        if trend in memory:
            prev = memory[trend]
            freq = prev["frequency"] + 1

            # running average
            new_avg = (
                (prev["avg_score"] * prev["frequency"]) + score
            ) / freq

            memory[trend].update({
                "last_seen": now,
                "frequency": freq,
                "avg_score": round(new_avg, 4)
            })
        else:
            memory[trend] = {
                "first_seen": now,
                "last_seen": now,
                "frequency": 1,
                "avg_score": round(score, 4)
            }

    _save_memory(memory)


# ---------------- SAVE ----------------
def _save_memory(memory: Dict[str, Dict]):
    with open(MEMORY_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()

        for trend, data in memory.items():
            writer.writerow({
                "trend": trend,
                **data
            })


# ---------------- CLI TEST ----------------
if __name__ == "__main__":
    test_trends = [
        {"trend": "openai agents", "score": 0.82},
        {"trend": "autonomous ai", "score": 0.75},
        {"trend": "openai agents", "score": 0.91},
    ]

    update_memory(test_trends)
    print("✅ Trend memory updated")
# agents/trend_memory.py

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# ---------------- PATHS ----------------
MEMORY_DIR = Path("data/memory")
MEMORY_FILE = MEMORY_DIR / "trend_memory.csv"

FIELDS = [
    "trend",
    "first_seen",
    "last_seen",
    "frequency",
    "avg_score"
]


# ---------------- INIT ----------------
def init_memory():
    """
    Initialize memory storage if not present.
    """
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    if not MEMORY_FILE.exists():
        with open(MEMORY_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


# ---------------- LOAD ----------------
def load_memory() -> Dict[str, Dict]:
    """
    Load memory into dict keyed by trend.
    """
    init_memory()
    memory = {}

    with open(MEMORY_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            memory[row["trend"]] = {
                "first_seen": row["first_seen"],
                "last_seen": row["last_seen"],
                "frequency": int(row["frequency"]),
                "avg_score": float(row["avg_score"])
            }

    return memory


# ---------------- UPDATE ----------------
def update_memory(trends: List[Dict]):
    """
    Update memory using newly detected trends.
    trends = [{"trend": str, "score": float}]
    """
    memory = load_memory()
    now = datetime.utcnow().isoformat()

    for item in trends:
        trend = item["trend"].lower().strip()
        score = float(item["score"])

        if trend in memory:
            prev = memory[trend]
            freq = prev["frequency"] + 1

            # running average
            new_avg = (
                (prev["avg_score"] * prev["frequency"]) + score
            ) / freq

            memory[trend].update({
                "last_seen": now,
                "frequency": freq,
                "avg_score": round(new_avg, 4)
            })
        else:
            memory[trend] = {
                "first_seen": now,
                "last_seen": now,
                "frequency": 1,
                "avg_score": round(score, 4)
            }

    _save_memory(memory)


# ---------------- SAVE ----------------
def _save_memory(memory: Dict[str, Dict]):
    with open(MEMORY_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()

        for trend, data in memory.items():
            writer.writerow({
                "trend": trend,
                **data
            })


# ---------------- CLI TEST ----------------
if __name__ == "__main__":
    test_trends = [
        {"trend": "openai agents", "score": 0.82},
        {"trend": "autonomous ai", "score": 0.75},
        {"trend": "openai agents", "score": 0.91},
    ]

    update_memory(test_trends)
    print("✅ Trend memory updated")
