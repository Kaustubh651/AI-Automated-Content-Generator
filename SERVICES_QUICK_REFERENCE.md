# Quick Reference: Services Organization

## Services Folder Structure

```
services/
├── writers/              Writers generate content
├── posters/              Posters send to platforms
├── content/              Content processing & generation
├── data/                 Data collection & analysis
├── trends/               Trend analysis & memory
└── infrastructure/       Base classes & patterns
```

## What Goes Where

### 📝 Writers Service
**Purpose:** Generate platform-specific content  
**Files:**
- `twitter_writer.py` - Tweet generation
- `medium_writer.py` - Article generation  
- `youtube_writer.py` - Script generation
- `llm_writer.py` - Generic writing

### 📤 Posters Service
**Purpose:** Post content to platforms  
**Files:**
- `twitter_poster.py` - Tweet posting
- `medium_poster.py` - Article posting
- `youtube_poster.py` - Video handling
- `instagram_poster.py` - Image posting
- `live_poster.py` - Orchestration
- `poster_factory.py` - Factory pattern

### 🎨 Content Service
**Purpose:** Process and prepare content  
**Files:**
- `llm_engine.py` - LLM management
- `content_generator.py` - Generation pipeline
- `content_refiner.py` - Cleanup & formatting
- `content_selector.py` - Selection logic
- `post_payload_builder.py` - Payload creation
- `image_generator.py` - Image generation

### 📊 Data Service
**Purpose:** Collect and analyze data  
**Files:**
- `news_scraper.py` - Web scraping
- `market_signal_collector.py` - Signal collection
- `market_signal_scorer.py` - Signal scoring

### 📈 Trends Service
**Purpose:** Analyze trending topics  
**Files:**
- `trend_memory.py` - History tracking
- `trend_evolution.py` - Progression analysis
- `trend_bias_engine.py` - Trend-based bias

### 🏗️ Infrastructure Service
**Purpose:** Base classes and patterns  
**Files:**
- `base_writer.py` - Writer interface
- `base_poster.py` - Poster interface
- `poster_factory.py` - Factory pattern

## Import Paths

### Old Style (Still Works)
```python
from agents.twitter_writer import write_twitter
from agents.twitter_poster import post_to_twitter
```

### New Style (Recommended)
```python
from services.writers import TwitterWriter, write_twitter
from services.posters import TwitterPoster, post_to_twitter
```

### By Service
```python
# Full service
from services import writers, posters, content, data, trends, infrastructure

# Specific items
from services.writers import TwitterWriter
from services.posters import PosterFactory
from services.content import LLMEngine
from services.data import scrape_news
from services.trends import load_memory
from services.infrastructure import BasePoster
```

## Common Tasks

### Add New Writer
1. Create file in `services/writers/` extending `BaseWriter`
2. Add to `services/writers/__init__.py`
3. Update `services/__init__.py`

### Add New Poster
1. Create file in `services/posters/` extending `BasePoster`
2. Add to `services/posters/__init__.py`
3. Register in `PosterFactory`
4. Update `services/__init__.py`

### Add New Service
1. Create folder in `services/`
2. Add files to new service
3. Create `__init__.py` with exports
4. Update `services/__init__.py`

## Benefits

✅ **Clear Organization** - Know where to find code  
✅ **Scalability** - Easy to add new features  
✅ **Team Development** - Clear ownership  
✅ **Maintenance** - Related code together  
✅ **Testing** - Isolated unit tests  
✅ **Backward Compatible** - Old code still works  

## File Count by Service

| Service | Files |
|---------|-------|
| writers | 5 |
| posters | 8 |
| content | 7 |
| data | 3 |
| trends | 3 |
| infrastructure | 3 |
| **Total** | **29** |

## Service Dependencies

```
infrastructure
    ↑
    ├─ writers (uses BaseWriter)
    └─ posters (uses BasePoster, PosterFactory)
        ↑
        ├─ content (LLMEngine, content generators)
        ├─ data (market signals, news)
        └─ trends (trend analysis)
```

## Example Usage

### Generate and Post Content
```python
from services.writers import TwitterWriter
from services.posters import TwitterPoster
from services.content import LLMEngine
from utils.config_loader import ConfigLoader

# Setup
config = ConfigLoader()
llm = LLMEngine(config=config.get_model_config())
writer = TwitterWriter(llm, config.get_platform_config("twitter"))
poster = TwitterPoster(config.get_platform_config("twitter"))

# Generate
content = writer.write("Your article here...")

# Post
from services.posters.base_poster import PostPayload
payload = PostPayload(platform="twitter", title="", content=content)
result = poster.post(payload)
```

### Use Factory (Simpler)
```python
from services.posters import PosterFactory

poster = PosterFactory.create("twitter")
result = poster.post(payload)
```

### Legacy Compatibility
```python
# Old code still works!
from agents.twitter_writer import write_twitter
from agents.twitter_poster import post_to_twitter

tweet = write_twitter(article)
post_to_twitter(tweet)
```

## Folder Location
```
c:\Users\kaustubh\OneDrive\Desktop\PROJECT-AUTOMATE\services\
```

## Documentation
See `SERVICES_ORGANIZATION.md` for detailed information.
