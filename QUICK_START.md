# Quick Reference: New Project Structure

## Where Things Are Now

### Content Writers (Platform-specific content generation)
**Location:** `services/writers/`

```python
from services.writers import TwitterWriter, write_twitter
from services.writers import MediumWriter, write_medium
from services.writers import YouTubeWriter, write_youtube
```

**Usage:**
```python
# Simple function interface
tweet = write_twitter("Article text here")
blog = write_medium("Article text here")  
script = write_youtube("Article text here")

# Class interface (advanced)
writer = TwitterWriter(llm_engine, config)
content = writer.write("Article text")
```

---

### Platform Posters (API posting implementations)
**Location:** `services/posters/`

```python
from services.posters import TwitterPoster, post_to_twitter
from services.posters import MediumPoster, post_to_medium, save_medium_draft
from services.posters import YouTubePoster, post_to_youtube, save_youtube_draft
from services.posters import post_to_instagram
```

**Usage:**
```python
# Simple function interface
post_to_twitter("Tweet content here")
post_to_medium("Article title", "Article content")
post_to_youtube("Video script here")
post_to_instagram("image.png", "Caption here")

# Class interface (advanced)
poster = TwitterPoster(config=config)
result = poster.post(payload)
```

---

### Content Generation (LLM-based)
**Location:** `services/meme_engine/`

```python
from services.meme_engine import generate_content, LLMEngine
```

**Usage:**
```python
# Main function
content = generate_content(
    article_text="...",
    platform="twitter",  # or "medium", "youtube"
    trend_status="STABLE"  # or "RISING", "FALLING"
)

# Low-level LLM access
llm = LLMEngine()
response = llm.generate("prompt here")
```

---

### Scoring & Trends
**Location:** `services/scoring_engine/`

```python
from services.scoring_engine import MarketSignalScorer
from services.scoring_engine import (
    collect_market_signals,
    update_trend_memory,
    apply_trend_bias
)
```

**Usage:**
```python
# Score market signals
scorer = MarketSignalScorer()
scored_signals = scorer.score(raw_signals)

# Trend analysis
signals = collect_market_signals()
update_trend_memory(signals)
biased_trends = apply_trend_bias(trends)
```

---

### News Scraping
**Location:** `services/scraper/`

```python
from services.scraper import scrape_news
```

**Usage:**
```python
scrape_news()  # Scrapes configured sources
# Saves to: data/raw/news_sample.csv
```

---

### Distribution & Posting
**Location:** `services/post_router/`

```python
from services.post_router import (
    LivePoster,
    post_live,
    build_post_payload
)
```

**Usage:**
```python
# Orchestrate posting to all platforms
poster = LivePoster(
    queue_dir=Path("data/post_queue"),
    enabled_platforms=["twitter", "medium", "youtube"],
    live_mode=True
)
results = poster.post_all()

# Or use convenience function
results = post_live()

# Build payload for queue
build_post_payload(trend="AI", platform="twitter")
```

---

### Base Classes & Factories
**Location:** `services/infrastructure/`

```python
from services.infrastructure import (
    BasePoster,
    BaseWriter,
    PostPayload,
    PosterFactory
)
```

**Usage:**
```python
# Create poster dynamically
poster = PosterFactory.create("twitter")

# Build payload
payload = PostPayload(
    platform="twitter",
    title="Tweet",
    content="Tweet content",
    tags=["ai", "tech"]
)
result = poster.post(payload)
```

---

### Configuration
**Location:** `shared/config/`

```python
from shared.config import get_config
```

**Usage:**
```python
config = get_config()

# Access nested config
api_key = config.get("twitter.api_key")
platforms = config.get("platforms")

# Check mode
if config.is_live_mode():
    # Real posting
    pass
else:
    # Preview/testing
    pass
```

---

### Utilities
**Location:** `shared/utils/`

```python
from shared.utils import OutputWriter
```

**Usage:**
```python
output = OutputWriter()
saved_path = output.save("Content here", "twitter")
```

---

## Common Workflows

### Generate & Post Content
```python
from services.meme_engine import generate_content
from services.posters import post_to_twitter

# Generate
content = generate_content(article_text="...", platform="twitter")

# Post
result = post_to_twitter(content)
```

### Run Full Pipeline
```python
# Daily content automation
python pipelines/daily_run.py

# Trend-driven content system
python pipelines/trend_driven_run.py
```

### Check What's Queued
```
# See payloads ready to post
ls data/post_queue/
```

### Test Without Posting
```python
config = get_config()
config.set_safe_mode(True)  # Won't actually post

poster = LivePoster()
results = poster.post_all()  # Preview only
```

---

## File Organization Summary

| Service | Location | Purpose |
|---------|----------|---------|
| Writers | `services/writers/` | Generate platform-specific content |
| Posters | `services/posters/` | Post to platforms |
| Content Gen | `services/meme_engine/` | LLM-based content generation |
| Scoring | `services/scoring_engine/` | Analyze market signals & trends |
| Scraper | `services/scraper/` | Collect news & data |
| Router | `services/post_router/` | Orchestrate distribution |
| Infrastructure | `services/infrastructure/` | Base classes & factories |
| Config | `shared/config/` | Configuration management |
| Utils | `shared/utils/` | Shared utilities |

---

## Migration Checklist (If Updating Old Code)

- [x] Change `from agents.` to `from services.`
- [x] Change `from utils.` to `from shared.`  
- [x] Update poster imports to `services.posters`
- [x] Update writer imports to `services.writers`
- [x] Update config imports to `shared.config`
- [x] Test imports: `python -c "from services import *; print('OK')"`
- [x] Run pipelines to verify end-to-end
