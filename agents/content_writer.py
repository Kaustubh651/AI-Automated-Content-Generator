# agent\content_writer.py -->unsued 🧹 Archive or move to /legacy
import json
from pathlib import Path

INPUT_PATH = "data/processed/news_with_opinion.json"
OUTPUT_DIR = "data/final"


def write_twitter(article):
    return f"""
🔥 {article['title']}

{article['stance']}

Why this matters 👇
{article['why_it_matters']}

My take:
{article['prediction']}

#Tech #AI #Startups
""".strip()


def write_medium(article):
    return f"""
# {article['title']}

## What happened?
{article['text']}

## Why this matters
{article['why_it_matters']}

## My opinion
{article['stance']}

## What’s next?
{article['prediction']}
""".strip()


def write_youtube(article):
    return f"""
[INTRO]
Today something BIG happened in tech.

{article['title']}

[BODY]
Here’s what’s going on:
{article['text']}

Why should you care?
{article['why_it_matters']}

My honest take:
{article['stance']}

[OUTRO]
If this trend continues,
{article['prediction']}

Like, subscribe, and see you tomorrow.
""".strip()


def main():
    articles = json.load(open(INPUT_PATH, "r", encoding="utf-8"))

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    for i, art in enumerate(articles):
        content = {
            "twitter": write_twitter(art),
            "medium": write_medium(art),
            "youtube": write_youtube(art),
            "source_url": art.get("url")
        }

        out_file = f"{OUTPUT_DIR}/content_{i}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)

        print(f"✅ Content generated → {out_file}")


if __name__ == "__main__":
    main()
