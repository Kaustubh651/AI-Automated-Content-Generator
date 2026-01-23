import pandas as pd
import json
from pathlib import Path

RAW_PATH = "data/raw/news_sample.csv"
OUT_PATH = "data/processed/selected_news.json"

KEYWORDS = [
    "ai", "artificial intelligence", "openai", "google",
    "microsoft", "startup", "tech", "machine learning",
    "llm", "genai", "cloud", "saas"
]


def is_relevant(title: str, text: str) -> bool:
    content = f"{title} {text}".lower()
    return any(k in content for k in KEYWORDS)


def select_top_news(df, top_n=1):
    df["is_relevant"] = df.apply(
        lambda x: is_relevant(x["title"], x["text"]),
        axis=1
    )

    relevant_df = df[df["is_relevant"]]

    if relevant_df.empty:
        relevant_df = df  # fallback

    return relevant_df.head(top_n)


def main():
    df = pd.read_csv(RAW_PATH)
    selected = select_top_news(df, top_n=1)

    Path("data/processed").mkdir(parents=True, exist_ok=True)

    output = []
    for _, row in selected.iterrows():
        output.append({
            "title": row["title"],
            "text": row["text"],
            "url": row["url"]
        })

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Selected {len(output)} article(s). Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
