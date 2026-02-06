#agent\opinion_agent.py
import json
from pathlib import Path

INPUT_PATH = "data/processed/selected_news.json"
OUTPUT_PATH = "data/processed/news_with_opinion.json"


def generate_opinion(article):
    """
    TEMP LOGIC (Sprint 1-A)
    Real LLM will replace this in next step
    """
    return {
        "stance": "This is a major shift in the tech industry.",
        "why_it_matters": "It impacts startups, developers, and future AI regulation.",
        "prediction": "More companies will copy this approach within 6–12 months."
    }


def main():
    articles = json.load(open(INPUT_PATH, "r", encoding="utf-8"))

    enriched = []
    for art in articles:
        opinion = generate_opinion(art)
        enriched.append({**art, **opinion})

    Path("data/processed").mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)

    print(f"✅ Opinion added → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
