# services/meme_engine/content_writer.py

import json
from pathlib import Path
from typing import Dict, Union

INPUT_PATH = "data/processed/news_with_opinion.json"
OUTPUT_DIR = "data/final"


def write_twitter(article: Union[Dict, str]) -> str:
    """Write Twitter content. Accepts either dict or string."""
    if isinstance(article, str):
        # If string, use it as title
        return f"""
🔥 {article[:100]}

Why this matters 👇
This is a significant development in tech.

My take:
Watch this space closely.

#Tech #AI #Startups
""".strip()
    
    # If dict, use the structured format
    return f"""
🔥 {article.get('title')}

{article.get('stance')}

Why this matters 👇
{article.get('why_it_matters')}

My take:
{article.get('prediction')}

#Tech #AI #Startups
""".strip()


def write_medium(article: Union[Dict, str]) -> str:
    """Write Medium content. Accepts either dict or string."""
    if isinstance(article, str):
        return f"""
# {article[:100]}

## What happened?
{article}

## Why this matters
This development has significant implications for the industry.

## My opinion
This is an important shift we should be paying attention to.

## What's next?
The industry will continue to evolve in interesting ways.
""".strip()
    
    # If dict, use the structured format
    return f"""
# {article.get('title')}

## What happened?
{article.get('text')}

## Why this matters
{article.get('why_it_matters')}

## My opinion
{article.get('stance')}

## What's next?
{article.get('prediction')}
""".strip()


def write_youtube(article: Union[Dict, str]) -> str:
    """Write YouTube script. Accepts either dict or string."""
    if isinstance(article, str):
        return f"""
[INTRO]
Today something BIG happened in tech.

[HEADLINE]
{article[:150]}

[BODY]
Let me break down what's happening and why it matters.

{article}

[OUTRO]
This is going to be a game-changer. Drop a like and subscribe for more insights.

[END]
""".strip()
    
    # If dict, use the structured format
    return f"""
[INTRO]
Today something BIG happened in tech.

[HEADLINE]
{article.get('title')}

[BODY]
{article.get('text')}

Why it matters: {article.get('why_it_matters')}

[OUTRO]
This is going to be a game-changer. Drop a like and subscribe for more insights.

[END]
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

