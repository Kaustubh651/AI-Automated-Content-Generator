# New Project Structure - Quick Reference

## Folder Overview

```
PROJECT-AUTOMATE/
├── services/              ← Core business logic (feature-based)
├── shared/                ← Reusable components (config, schemas, utils)
├── experiments/           ← ML/DL testing (never import into prod)
├── pipelines/             ← Orchestration workflows
├── tests/                 ← Unit/integration tests
├── config/                ← Configuration files
├── data/                  ← Data storage (raw, processed, memory)
└── docs/                  ← Documentation
```

## Services at a Glance

| Service | Purpose | Location | Key Modules |
|---------|---------|----------|------------|
| **scraper** | Collect news data | `services/scraper/` | `news_scraper.py` |
| **scoring_engine** | Analyze signals, trends, quality | `services/scoring_engine/` | `market_signal_scorer.py`, `trend_memory.py` |
| **meme_engine** | Generate content via LLM | `services/meme_engine/` | `llm_engine.py`, `content_generator.py` |
| **post_router** | Route & post to platforms | `services/post_router/` | `live_poster.py`, `twitter_poster.py`, `medium_poster.py` |
| **instagram_poster** | Instagram-specific posting | `services/instagram_poster/` | `instagram_poster.py` |

## Shared Module at a Glance

| Module | Purpose | Key Classes |
|--------|---------|------------|
| **schemas** | Data contracts | `PostPayload`, `ContentPayload`, `SignalPayload` |
| **config** | Configuration management | `ConfigLoader`, `get_config()` |
| **utils** | Utility functions | `OutputWriter`, `load_json()`, `sanitize_text()` |

## Common Tasks

### Load Configuration
```python
from shared.config import get_config
config = get_config()
model_name = config.get("model.name")
```

### Generate Content
```python
from services.meme_engine import ContentGenerator
from shared.config import get_config

gen = ContentGenerator(config=get_config())
content = gen.generate("article text")
```

### Post to Platform
```python
from services.post_router import LivePoster
from shared.config import get_config

poster = LivePoster(config=get_config())
poster.post_content("content", "twitter")
```

### Score Market Signals
```python
from services.scoring_engine import MarketSignalScorer

scorer = MarketSignalScorer()
score = scorer.score(signal_data)
```

### Save Output
```python
from shared.utils import OutputWriter

writer = OutputWriter()
path = writer.save("content", "twitter")
```

## Backward Compatibility

All old imports still work! Both work:
```python
# Old way (still works)
from agents.content_generator import ContentGenerator

# New way (recommended)
from services.meme_engine import ContentGenerator
```

## File Organization Strategy

**When you need to add code, ask:**
- Is it **data collection**? → `services/scraper/`
- Is it **analysis/scoring**? → `services/scoring_engine/`
- Is it **content generation**? → `services/meme_engine/`
- Is it **posting/routing**? → `services/post_router/`
- Is it **Instagram only**? → `services/instagram_poster/`
- Is it **configuration**? → `shared/config/`
- Is it **data format**? → `shared/schemas/`
- Is it **utility function**? → `shared/utils/`
- Is it **experimental**? → `experiments/`

## Next Steps

1. **Review** `docs/ARCHITECTURE.md` for full details
2. **Read** `docs/MIGRATION_GUIDE.md` for import examples
3. **Update** `pipelines/*.py` to use new imports (optional, backward compat works)
4. **Add** new features to appropriate services
5. **Experiment** safely in `experiments/` folder

## Adding a New Service

```bash
# 1. Create folder
mkdir services/new_service

# 2. Create __init__.py
echo 'from services.new_service.core import MyService' > services/new_service/__init__.py

# 3. Create implementation
# services/new_service/core.py
class MyService:
    def __init__(self, config=None):
        self.config = config
    def operate(self, data):
        pass

# 4. Use it
from services.new_service import MyService
service = MyService()
```

## Architecture Benefits

✅ **Modular** - Each service independent  
✅ **Testable** - Services test in isolation  
✅ **Scalable** - New services without breaking existing code  
✅ **Maintainable** - Clear responsibility boundaries  
✅ **Flexible** - Easy to swap implementations  
✅ **Reusable** - Shared utilities everywhere  
✅ **Compatible** - Old code keeps working  
✅ **Experimental** - Safe testing in experiments/  

## Import Quick Reference

```python
# Config
from shared.config import get_config

# Schemas
from shared.schemas import PostPayload, ContentPayload, SignalPayload

# Utilities
from shared.utils import OutputWriter, load_json, save_json

# Services
from services.scraper import NewsScraper
from services.scoring_engine import MarketSignalScorer, TrendMemory
from services.meme_engine import ContentGenerator, LLMEngine
from services.post_router import LivePoster, TwitterPoster
from services.instagram_poster import InstagramPoster
```

## Configuration

Set all config in `config/config.yaml`:
```yaml
model:
  name: "Zephyr-7b"
  temperature: 0.7

platforms:
  twitter:
    enabled: true
    max_tokens: 280
```

Access via:
```python
from shared.config import get_config
config = get_config()
model_name = config.get("model.name")
```

---

**Last Updated:** 2026-02-10  
**Architecture Version:** 2.0 (Services-based)
