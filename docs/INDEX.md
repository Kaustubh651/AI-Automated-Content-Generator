# Documentation Index

Welcome to PROJECT-AUTOMATE documentation! This is your guide to understanding and working with the codebase.

## 📖 Main Documentation

### [ARCHITECTURE.md](ARCHITECTURE.md)
**The comprehensive guide to the entire system**
- Complete folder structure and organization
- Detailed service descriptions (scraper, scoring_engine, meme_engine, post_router, instagram_poster)
- Shared module details (schemas, config, utils)
- Experiments module guidelines
- Import patterns and examples
- How to add new services
- Configuration details
- Testing strategies
- Benefits of the new architecture
- Migration path

**Read this if:** You want to understand how everything fits together

---

### [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
**Step-by-step guide for updating your code**
- File organization map (old location → new location)
- Import migration examples with before/after code
- Backward compatibility information
- Migration checklist
- Benefits of the new structure
- How to add new services to the new structure

**Read this if:** You're upgrading from the old structure or updating imports

---

### [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
**Fast lookup for common tasks**
- Folder overview at a glance
- Services summary table
- Shared module summary
- Common tasks with code examples
- Backward compatibility notice
- File organization strategy
- Performance considerations

**Read this if:** You need a quick answer without reading full docs

---

## 🎯 Quick Navigation

### I want to...

#### Understand the project structure
→ Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for overview
→ Then read [ARCHITECTURE.md](ARCHITECTURE.md) for deep dive

#### Update my code to use new imports
→ Read [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
→ Compare before/after examples

#### Add a new feature
→ Check [ARCHITECTURE.md - Adding a New Service](ARCHITECTURE.md#adding-a-new-service)
→ Or add to existing service in [ARCHITECTURE.md - Service Architecture](ARCHITECTURE.md#service-architecture)

#### Understand data contracts
→ See [ARCHITECTURE.md - Shared Module](ARCHITECTURE.md#shared-module)
→ Look at [payloads.py](../shared/schemas/payloads.py)

#### Learn about configuration
→ Read [ARCHITECTURE.md - Configuration](ARCHITECTURE.md#configuration)
→ Edit [config.yaml](../config/config.yaml)

#### Write tests
→ Check [ARCHITECTURE.md - Testing](ARCHITECTURE.md#testing)
→ Look at existing tests in [tests/](../tests/)

#### Understand imports
→ Quick lookup: [QUICK_REFERENCE.md - Import Quick Reference](QUICK_REFERENCE.md#import-quick-reference)
→ Detailed: [MIGRATION_GUIDE.md - Import Migration Examples](MIGRATION_GUIDE.md#import-migration-examples)

---

## 📚 Service Guides

Quick access to service documentation:

### [services/scraper/](../services/scraper/)
News data collection service
```python
from services.scraper import NewsScraper
scraper = NewsScraper()
news = scraper.fetch_news(query="AI")
```

### [services/scoring_engine/](../services/scoring_engine/)
Signal analysis and trend tracking
```python
from services.scoring_engine import MarketSignalScorer, TrendMemory
scorer = MarketSignalScorer()
score = scorer.score(signal_data)
```

### [services/meme_engine/](../services/meme_engine/)
Content generation via LLM
```python
from services.meme_engine import ContentGenerator
from shared.config import get_config

gen = ContentGenerator(config=get_config())
content = gen.generate("article text")
```

### [services/post_router/](../services/post_router/)
Distribution and posting orchestration
```python
from services.post_router import LivePoster
from shared.config import get_config

poster = LivePoster(config=get_config())
poster.post_content("content", "twitter")
```

### [services/instagram_poster/](../services/instagram_poster/)
Instagram-specific operations
```python
from services.instagram_poster import InstagramPoster
poster = InstagramPoster()
poster.post(content="...", image_path="...")
```

---

## 🔧 Configuration

All configuration in one place:
- **YAML Config:** [config/config.yaml](../config/config.yaml) - Main settings
- **Secrets:** [config/secrets.env](../config/secrets.env) - API keys
- **Loader:** [shared/config/config_loader.py](../shared/config/config_loader.py) - Access config

**Load config:**
```python
from shared.config import get_config
config = get_config()
```

---

## 📦 Shared Components

Reusable across all services:

### Schemas (Data Contracts)
```python
from shared.schemas import PostPayload, ContentPayload, SignalPayload
```

### Config (Configuration Management)
```python
from shared.config import get_config, ConfigLoader
```

### Utils (Utilities)
```python
from shared.utils import OutputWriter, load_json, save_json, sanitize_text
```

---

## 🧪 Experiments

Safe testing ground (never import into production):
```
experiments/
├── model_training/
├── a_b_testing/
├── performance_bench/
└── feature_research/
```

**Do NOT use:**
```python
# ❌ Never do this in production code
from experiments import something
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────┐
│           External Data Sources             │
│     (News, Social Media, Market Data)       │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│      services/scraper/                      │
│    (News Collection & Parsing)              │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│   services/scoring_engine/                  │
│  (Signal Analysis, Trend Tracking)          │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│    services/meme_engine/                    │
│  (LLM-Based Content Generation)             │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│    services/post_router/                    │
│  (Platform Routing & Distribution)          │
└────┬─────────────┬──────────┬──────────┬────┘
     │             │          │          │
     ▼             ▼          ▼          ▼
  Twitter       Medium    YouTube   Instagram
  (Twitter)   (Medium)  (YouTube)   (Custom)
     │             │          │          │
     └─────────────┴──────────┴──────────┘
              │
              ▼
      Published Content
```

---

## 🔄 Backward Compatibility

Old code still works! But we recommend updating:

**Old (Still Works):**
```python
from agents.content_generator import ContentGenerator
```

**New (Recommended):**
```python
from services.meme_engine import ContentGenerator
```

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for details.

---

## 📝 File Reference

| File | Purpose |
|------|---------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Complete architectural documentation |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | Import migration with examples |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick lookup tables |
| [INDEX.md](INDEX.md) | This file - navigation guide |

---

## 🆘 Common Questions

**Q: Where do I put my new feature?**  
A: Follow the service it belongs to:
- Data collection → `services/scraper/`
- Analysis → `services/scoring_engine/`
- Content generation → `services/meme_engine/`
- Posting/routing → `services/post_router/`
- Instagram → `services/instagram_poster/`
- Config → `shared/config/`
- Utilities → `shared/utils/`

**Q: Can I still use old imports?**  
A: Yes! See backward compatibility in [QUICK_REFERENCE.md](QUICK_REFERENCE.md#backward-compatibility)

**Q: How do I add a new service?**  
A: See [ARCHITECTURE.md - Adding a New Service](ARCHITECTURE.md#adding-a-new-service)

**Q: Where's the configuration?**  
A: [config/config.yaml](../config/config.yaml) - All settings in one place

**Q: How do I test my code?**  
A: See [ARCHITECTURE.md - Testing](ARCHITECTURE.md#testing)

**Q: Can I experiment safely?**  
A: Use [experiments/](../experiments/) folder - never imported in production

---

## 📞 Need Help?

1. **Lost?** → Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **Confused?** → Read [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Updating code?** → Read [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
4. **Quick lookup?** → Use this [INDEX.md](INDEX.md)

---

**Last Updated:** 2026-02-10  
**Version:** 2.0 (Services Architecture)
