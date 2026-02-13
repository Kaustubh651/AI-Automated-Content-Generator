# PROJECT-AUTOMATE: Scalable Architecture

## Overview

This document describes the new scalable architecture for PROJECT-AUTOMATE, designed to support multiple projects, experiments, and features while maintaining clean separation of concerns.

## Directory Structure

```
PROJECT-AUTOMATE/
│
├── services/                    # Core business logic (feature-based)
│   ├── scraper/                 # News data collection
│   │   ├── __init__.py
│   │   ├── news_scraper.py
│   │   └── ...
│   │
│   ├── scoring_engine/          # Signal analysis and scoring
│   │   ├── __init__.py
│   │   ├── market_signal_collector.py
│   │   ├── market_signal_scorer.py
│   │   ├── trend_memory.py
│   │   ├── trend_evolution.py
│   │   ├── trend_bias_engine.py
│   │   └── ...
│   │
│   ├── meme_engine/             # Content generation (LLM-based)
│   │   ├── __init__.py
│   │   ├── llm_engine.py
│   │   ├── content_generator.py
│   │   ├── content_refiner.py
│   │   ├── content_selector.py
│   │   ├── content_writer.py
│   │   └── ...
│   │
│   ├── post_router/             # Distribution and routing
│   │   ├── __init__.py
│   │   ├── live_poster.py
│   │   ├── twitter_writer.py
│   │   ├── medium_writer.py
│   │   ├── youtube_writer.py
│   │   ├── twitter_poster.py
│   │   ├── medium_poster.py
│   │   ├── youtube_poster.py
│   │   ├── platform_poster.py
│   │   ├── post_payload_builder.py
│   │   └── ...
│   │
│   ├── instagram_poster/        # Instagram-specific
│   │   ├── __init__.py
│   │   └── instagram_poster.py
│   │
│   ├── writers/                 # [LEGACY] Maintained for backward compat
│   ├── posters/                 # [LEGACY] Maintained for backward compat
│   ├── content/                 # [LEGACY] Maintained for backward compat
│   ├── data/                    # [LEGACY] Maintained for backward compat
│   ├── trends/                  # [LEGACY] Maintained for backward compat
│   └── infrastructure/          # [LEGACY] Base classes and patterns
│
├── shared/                      # Cross-cutting concerns
│   ├── schemas/                 # Data contracts
│   │   ├── __init__.py
│   │   └── payloads.py
│   │
│   ├── config/                  # Configuration management
│   │   ├── __init__.py
│   │   └── config_loader.py
│   │
│   ├── utils/                   # Pure utility functions
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   ├── output_writer.py
│   │   └── ...
│   │
│   └── __init__.py
│
├── experiments/                 # ML/DL research only (NOT production)
│   ├── __init__.py
│   ├── model_training/
│   ├── a_b_testing/
│   ├── performance_bench/
│   └── ...
│
├── docs/                        # Project documentation
│   └── ...
│
├── config/                      # Configuration files
│   ├── config.yaml
│   └── secrets.env
│
├── data/                        # Data storage
│   ├── raw/
│   ├── processed/
│   ├── memory/
│   ├── post_queue/
│   └── final/
│
├── pipelines/                   # Orchestration workflows
│   ├── daily_run.py
│   ├── trend_driven_run.py
│   └── ...
│
├── tests/                       # Unit and integration tests
│   └── ...
│
└── README.md
```

## Service Architecture

### 1. Scraper Service
**Purpose:** Collect news data from various sources
**Location:** `services/scraper/`
**Key Classes:**
- `NewsScraper` - Main scraper interface
- `NewsParser` - Parse and normalize news

**Usage:**
```python
from services.scraper import NewsScraper
scraper = NewsScraper()
news = scraper.fetch_news(query="AI")
```

### 2. Scoring Engine Service
**Purpose:** Analyze signals, trends, and content quality
**Location:** `services/scoring_engine/`
**Key Classes:**
- `MarketSignalCollector` - Collect market signals
- `MarketSignalScorer` - Score signal importance
- `TrendMemory` - Remember trend history
- `TrendEvolution` - Track trend changes
- `TrendBiasEngine` - Detect and correct biases

**Usage:**
```python
from services.scoring_engine import MarketSignalScorer
scorer = MarketSignalScorer()
score = scorer.score_signal(signal_data)
```

### 3. Meme Engine Service
**Purpose:** Generate content using LLM
**Location:** `services/meme_engine/`
**Key Classes:**
- `LLMEngine` - Core LLM inference
- `ContentGenerator` - Generate platform-specific content
- `ContentRefiner` - Clean and optimize content
- `ContentSelector` - Choose best content variants
- `ContentWriter` - Format content for output

**Usage:**
```python
from services.meme_engine import ContentGenerator
from shared.config import get_config

gen = ContentGenerator(config=get_config())
content = gen.generate(article_text="...")
```

### 4. Post Router Service
**Purpose:** Route content to platforms and manage posting
**Location:** `services/post_router/`
**Key Classes:**
- `LivePoster` - Orchestrate posting across platforms
- `TwitterWriter` / `TwitterPoster` - Twitter specifics
- `MediumWriter` / `MediumPoster` - Medium specifics
- `YouTubeWriter` / `YouTubePoster` - YouTube specifics
- `PlatformPoster` - Base platform interface
- `PostPayloadBuilder` - Construct posting payloads

**Usage:**
```python
from services.post_router import LivePoster
from shared.config import get_config

poster = LivePoster(config=get_config())
poster.post_content(content="...", platform="twitter")
```

### 5. Instagram Poster Service
**Purpose:** Instagram-specific posting operations
**Location:** `services/instagram_poster/`
**Key Classes:**
- `InstagramPoster` - Handle Instagram API calls
- `InstagramOptimizer` - Optimize for Instagram format

**Usage:**
```python
from services.instagram_poster import InstagramPoster
poster = InstagramPoster()
poster.post(content="...", image_path="...")
```

## Shared Module

### Schemas (`shared/schemas/`)
Define data contracts used across services:
- `PostPayload` - Standard posting format
- `ContentPayload` - Generated content format
- `SignalPayload` - Market signal format

**Usage:**
```python
from shared.schemas import PostPayload

payload = PostPayload(
    content="...",
    platform="twitter",
    tags=["AI", "tech"]
)
```

### Config (`shared/config/`)
Centralized configuration management:
- `ConfigLoader` - Singleton config access
- `get_config()` - Get global config instance

**Usage:**
```python
from shared.config import get_config

config = get_config()
model_name = config.get("model.name")
```

### Utils (`shared/utils/`)
Pure utility functions:
- `OutputWriter` - Save content to disk
- `load_json()` / `save_json()` - JSON operations
- `sanitize_text()` - Clean text
- `chunk_text()` - Split text into chunks

**Usage:**
```python
from shared.utils import OutputWriter, load_json

writer = OutputWriter()
path = writer.save(content, "twitter")
data = load_json("data.json")
```

## Experiments Module

**Purpose:** Testing ground for ML/DL experiments
**Location:** `experiments/`
**Usage:** Do NOT import from experiments in production code

**Suggested Structure:**
```
experiments/
├── model_training/      # Train new models
├── a_b_testing/         # Compare variants
├── performance_bench/   # Benchmark different approaches
└── feature_research/    # Explore new features
```

## Import Patterns

### New Preferred Style (Using New Structure)
```python
# Service imports
from services.scraper import NewsScraper
from services.scoring_engine import MarketSignalScorer
from services.meme_engine import ContentGenerator
from services.post_router import LivePoster

# Shared imports
from shared.config import get_config
from shared.schemas import PostPayload
from shared.utils import OutputWriter
```

### Legacy Style (Still Supported)
```python
# Old imports still work due to backward compatibility
from services.writers import write_twitter
from services.posters import post_to_twitter
from agents.content_generator import ContentGenerator
```

## Dependency Injection Pattern

All services receive dependencies via constructor:

```python
from services.meme_engine import ContentGenerator
from shared.config import get_config

config = get_config()
gen = ContentGenerator(config=config)
content = gen.generate(text)
```

## Adding a New Service

1. **Create service folder:**
   ```
   mkdir services/my_service
   touch services/my_service/__init__.py
   ```

2. **Define service interface:**
   ```python
   # services/my_service/core.py
   class MyService:
       def __init__(self, config=None):
           self.config = config or get_config()
       
       def operation(self, data):
           pass
   ```

3. **Export from __init__.py:**
   ```python
   # services/my_service/__init__.py
   from services.my_service.core import MyService
   __all__ = ['MyService']
   ```

4. **Use in your code:**
   ```python
   from services.my_service import MyService
   service = MyService()
   result = service.operation(data)
   ```

## Configuration

All configuration goes in `config/config.yaml`. Environment secrets in `config/secrets.env`.

**Example config.yaml:**
```yaml
model:
  name: "Zephyr-7b"
  temperature: 0.7
  max_tokens: 500

platforms:
  twitter:
    enabled: true
    max_tokens: 280
  medium:
    enabled: true
    max_tokens: 600

posting:
  live_mode: true
  enabled_platforms:
    - twitter
    - medium
    - youtube
```

## Testing

Each service should have its own tests:
```
tests/
├── test_scraper.py
├── test_scoring_engine.py
├── test_meme_engine.py
├── test_post_router.py
└── ...
```

**Test a service in isolation:**
```python
from services.meme_engine import ContentGenerator
from shared.config import get_config

def test_content_generation():
    gen = ContentGenerator(config=get_config())
    result = gen.generate("test article")
    assert result is not None
```

## Benefits of This Architecture

1. **Modularity:** Each service is self-contained
2. **Testability:** Services can be tested independently
3. **Scalability:** New services can be added without affecting existing code
4. **Maintainability:** Clear responsibility boundaries
5. **Reusability:** Shared utilities available to all services
6. **Flexibility:** Easy to swap implementations
7. **Backward Compatibility:** Legacy code continues to work
8. **Experimentation:** Isolated experiments don't affect production

## Migration Path

Existing code continues to work via backward compatibility layer. Gradually migrate to new structure:

**Phase 1 (Current):** New structure defined, old imports work
**Phase 2:** Update pipelines to use new service imports
**Phase 3:** Create additional projects in same workspace
**Phase 4:** Introduce shared utilities across projects
