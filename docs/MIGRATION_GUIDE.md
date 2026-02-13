# Migration Guide: New Service Architecture

## Quick Start

The new architecture is now active. Your code can use both old and new import styles, but we recommend transitioning to the new structure.

## File Organization Map

| Purpose | Old Location | New Location |
|---------|--------------|--------------|
| News scraping | `agents/news_scraper.py` | `services/scraper/news_scraper.py` |
| Signal scoring | `agents/market_signal_scorer.py` | `services/scoring_engine/market_signal_scorer.py` |
| Signal collection | `agents/market_signal_collector.py` | `services/scoring_engine/market_signal_collector.py` |
| Trend tracking | `agents/trend_memory.py` | `services/scoring_engine/trend_memory.py` |
| Trend evolution | `agents/trend_evolution.py` | `services/scoring_engine/trend_evolution.py` |
| Trend bias | `agents/trend_bias_engine.py` | `services/scoring_engine/trend_bias_engine.py` |
| LLM inference | `agents/llm_engine.py` | `services/meme_engine/llm_engine.py` |
| Content generation | `agents/content_generator.py` | `services/meme_engine/content_generator.py` |
| Content refinement | `agents/content_refiner.py` | `services/meme_engine/content_refiner.py` |
| Content selection | `agents/content_selector.py` | `services/meme_engine/content_selector.py` |
| Content writing | `agents/content_writer.py` | `services/meme_engine/content_writer.py` |
| Twitter writing | `agents/twitter_writer.py` | `services/post_router/twitter_writer.py` |
| Medium writing | `agents/medium_writer.py` | `services/post_router/medium_writer.py` |
| YouTube writing | `agents/youtube_writer.py` | `services/post_router/youtube_writer.py` |
| Twitter posting | `agents/twitter_poster.py` | `services/post_router/twitter_poster.py` |
| Medium posting | `agents/medium_poster.py` | `services/post_router/medium_poster.py` |
| YouTube posting | `agents/youtube_poster.py` | `services/post_router/youtube_poster.py` |
| Instagram posting | `agents/instagram_poster.py` | `services/instagram_poster/instagram_poster.py` |
| Live posting | `agents/live_poster.py` | `services/post_router/live_poster.py` |
| Payload building | `agents/post_payload_builder.py` | `services/post_router/post_payload_builder.py` |
| Config loading | `utils/config_loader.py` | `shared/config/config_loader.py` |
| Output writing | `utils/output_writer.py` | `shared/utils/output_writer.py` |

## Import Migration Examples

### Example 1: Config Loading

**Old:**
```python
from utils.config_loader import ConfigLoader
config = ConfigLoader()
```

**New (Recommended):**
```python
from shared.config import get_config
config = get_config()
```

### Example 2: Content Generation

**Old:**
```python
from agents.content_generator import ContentGenerator
from agents.llm_engine import LLMEngine

llm = LLMEngine()
gen = ContentGenerator(llm)
```

**New (Recommended):**
```python
from services.meme_engine import ContentGenerator
from shared.config import get_config

gen = ContentGenerator(config=get_config())
content = gen.generate("article text")
```

### Example 3: Posting Content

**Old:**
```python
from agents.live_poster import LivePoster
from agents.content_generator import ContentGenerator

poster = LivePoster()
gen = ContentGenerator()
content = gen.generate("news")
poster.post_content(content, "twitter")
```

**New (Recommended):**
```python
from services.post_router import LivePoster
from services.meme_engine import ContentGenerator
from shared.config import get_config

config = get_config()
gen = ContentGenerator(config=config)
poster = LivePoster(config=config)
content = gen.generate("news")
poster.post_content(content, "twitter")
```

### Example 4: Scoring Signals

**Old:**
```python
from agents.market_signal_scorer import MarketSignalScorer

scorer = MarketSignalScorer()
score = scorer.score(signal_data)
```

**New (Recommended):**
```python
from services.scoring_engine import MarketSignalScorer

scorer = MarketSignalScorer()
score = scorer.score(signal_data)
```

### Example 5: Using Utilities

**Old:**
```python
from utils.output_writer import save_output

path = save_output("content", "twitter")
```

**New (Recommended):**
```python
from shared.utils import OutputWriter

writer = OutputWriter()
path = writer.save("content", "twitter")
```

## Backward Compatibility

All old imports continue to work! You can keep using old imports or transition gradually:

```python
# Old imports still work (via agents/__init__.py backward compatibility)
from agents.content_generator import ContentGenerator

# But new imports are cleaner
from services.meme_engine import ContentGenerator
```

## Migration Checklist

- [ ] Review `docs/ARCHITECTURE.md` for new structure
- [ ] Update pipeline imports in `pipelines/daily_run.py`
- [ ] Update pipeline imports in `pipelines/trend_driven_run.py`
- [ ] Test that services can be imported: `python -c "from services import *"`
- [ ] Update config paths if needed (should auto-detect)
- [ ] Run existing tests to verify backward compatibility
- [ ] Gradually update new code to use new imports

## Benefits of Moving to New Structure

1. **Clarity:** Service names clearly indicate purpose
   - `services/meme_engine/` → Content generation
   - `services/scoring_engine/` → Analysis
   - `services/post_router/` → Distribution

2. **Scalability:** Easy to understand where to add features
   - New scraper? Add to `services/scraper/`
   - New scoring logic? Add to `services/scoring_engine/`

3. **Maintainability:** Clear boundaries between concerns
   - Content generation separate from posting
   - Scoring separate from scraping

4. **Testing:** Services can be tested in isolation
   - Mock dependencies easily
   - Test without running full pipeline

5. **Experimentation:** Isolated experiments folder
   - `experiments/` never imported into production
   - Safe place for A/B testing

## Adding Future Services

When you need a new feature, simply create a new service:

```bash
# Create new service
mkdir services/my_new_feature
touch services/my_new_feature/__init__.py
touch services/my_new_feature/core.py

# Implement your service
# Update services/my_new_feature/__init__.py with exports
# Use it immediately
```

Example:
```python
from services.my_new_feature import MyService

service = MyService()
result = service.do_something()
```

## Performance Considerations

The new architecture has minimal overhead:
- Imports are the same (no runtime cost)
- Services use same Singleton pattern for config
- Backward compatibility adds ~50 re-exports (negligible)
- No performance degradation

## Questions?

Refer to `docs/ARCHITECTURE.md` for comprehensive documentation.
