# Migration Guide: From Old to New Architecture

This guide shows how to migrate existing code to use the new modular architecture.

## Content Generation Pipeline

### Old Code (Still Works)
```python
from agents.twitter_writer import write_twitter
from agents.content_generator import generate_content

# Old way - uses global LLM
content = generate_content(article_text, "twitter")
tweet = write_twitter(article_text)
```

### New Code (Recommended)
```python
from agents.twitter_writer import TwitterWriter
from agents.content_generator import ContentGenerator
from agents.llm_engine import LLMEngine
from utils.config_loader import ConfigLoader

# New way - dependency injection
config_loader = ConfigLoader()
llm = LLMEngine(config=config_loader.get_model_config())

# Create generator with injected dependencies
generator = ContentGenerator(
    llm_engine=llm,
    config=config_loader.get_all()
)

# Generate content with explicit config
content = generator.generate(
    article_text="...",
    platform="twitter",
    use_market_signals=True
)
```

## Direct Writer Usage

### Old Code (Still Works)
```python
from agents.twitter_writer import write_twitter
from agents.medium_writer import write_medium
from agents.youtube_writer import write_youtube

twitter_content = write_twitter(article)
medium_content = write_medium(article)
youtube_content = write_youtube(article)
```

### New Code (Recommended)
```python
from agents.twitter_writer import TwitterWriter
from agents.medium_writer import MediumWriter
from agents.youtube_writer import YouTubeWriter
from agents.llm_engine import LLMEngine
from utils.config_loader import ConfigLoader

config_loader = ConfigLoader()
llm = LLMEngine(config=config_loader.get_model_config())

twitter_writer = TwitterWriter(
    llm_engine=llm,
    config=config_loader.get_platform_config("twitter")
)

medium_writer = MediumWriter(
    llm_engine=llm,
    config=config_loader.get_platform_config("medium")
)

youtube_writer = YouTubeWriter(
    llm_engine=llm,
    config=config_loader.get_platform_config("youtube")
)

twitter_content = twitter_writer.write(article)
medium_content = medium_writer.write(article)
youtube_content = youtube_writer.write(article)
```

## Live Posting

### Old Code (Still Works)
```python
from agents.live_poster import post_live

post_live()  # Uses global config
```

### New Code (Recommended)
```python
from agents.live_poster import LivePoster
from pathlib import Path

# Use dependency injection for customization
poster = LivePoster(
    queue_dir=Path("data/post_queue"),
    enabled_platforms=["twitter", "medium", "youtube"],
    live_mode=False  # Test mode
)

results = poster.post_all()
```

## Platform-Specific Posting

### Old Code (Still Works)
```python
from agents.twitter_poster import post_to_twitter
from agents.medium_poster import post_to_medium

post_to_twitter("Hello world!")
post_to_medium("Article title", "Article content")
```

### New Code (Recommended)
```python
from agents.poster_factory import PosterFactory
from agents.base_poster import PostPayload

# Twitter
twitter_poster = PosterFactory.create("twitter")
payload = PostPayload(
    platform="twitter",
    title="",
    content="Hello world!"
)
result = twitter_poster.post(payload)

# Medium
medium_poster = PosterFactory.create("medium")
payload = PostPayload(
    platform="medium",
    title="Article title",
    content="Article content",
    tags=["tech", "ai"]
)
result = medium_poster.post(payload)
```

## Configuration Management

### Old Code (Still Works)
```python
from utils.config_loader import load_config

config = load_config()
model_name = config["model"]["name"]
platforms = config["platforms"]
```

### New Code (Recommended)
```python
from utils.config_loader import ConfigLoader

config = ConfigLoader()

# Access with dot notation
model_name = config.get("model.name")
max_tokens = config.get("model.max_tokens", 512)

# Specific getters
model_config = config.get_model_config()
enabled_platforms = config.get_enabled_platforms()
is_live = config.is_live_mode()

# Get entire config
all_config = config.get_all()
```

## Adding a New Platform - Complete Example

Let's say you want to add **LinkedIn** posting.

### Step 1: Create LinkedIn Writer (Optional)
```python
# agents/linkedin_writer.py
from agents.base_writer import BaseWriter

class LinkedInWriter(BaseWriter):
    """LinkedIn-specific content writer."""
    
    def get_system_prompt(self) -> str:
        return """You are a professional LinkedIn thought leader.
        
Write an engaging LinkedIn post about the article.
Requirements:
- Professional but personable tone
- 3-5 paragraphs
- Include relevant hashtags
- End with a question to encourage engagement"""
    
    def get_max_tokens(self) -> int:
        return self.config.get("max_tokens", 400)


# Legacy function for backward compatibility
def write_linkedin(article_text: str) -> str:
    from agents.llm_engine import LLMEngine
    from utils.config_loader import ConfigLoader
    
    config = ConfigLoader().get_platform_config("linkedin")
    llm = LLMEngine()
    writer = LinkedInWriter(llm, config)
    return writer.write(article_text)
```

### Step 2: Create LinkedIn Poster
```python
# agents/linkedin_poster.py
import os
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

from agents.base_poster import BasePoster, PostPayload

load_dotenv("config/secrets.env")

class LinkedInPoster(BasePoster):
    """Posts to LinkedIn."""
    
    def _validate_config(self):
        """Validate LinkedIn credentials."""
        if not os.getenv("LINKEDIN_ACCESS_TOKEN"):
            raise EnvironmentError("LINKEDIN_ACCESS_TOKEN not found")
    
    def post(self, payload: PostPayload) -> Dict[str, Any]:
        """Post to LinkedIn."""
        return self._safe_post(
            self._post_impl,
            payload.content,
            payload.tags
        )
    
    def _post_impl(self, content: str, tags: list) -> Dict[str, Any]:
        """Internal posting implementation."""
        import requests
        
        token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        headers = {"Authorization": f"Bearer {token}"}
        
        # LinkedIn API call
        response = requests.post(
            "https://api.linkedin.com/v2/posts",
            headers=headers,
            json={
                "content": content,
                "shareMediaCategory": "ARTICLE"
            }
        )
        
        response.raise_for_status()
        
        post_id = response.json()["id"]
        url = f"https://linkedin.com/feed/update/{post_id}/"
        
        self._log(f"Posted to LinkedIn: {url}")
        
        return {
            "url": url,
            "post_id": post_id,
            "timestamp": datetime.utcnow().isoformat()
        }


def post_to_linkedin(content: str):
    """Legacy function for compatibility."""
    from utils.config_loader import ConfigLoader
    
    config = ConfigLoader().get_platform_config("linkedin")
    poster = LinkedInPoster(config=config)
    
    payload = PostPayload(
        platform="linkedin",
        title="",
        content=content
    )
    
    return poster.post(payload)
```

### Step 3: Add to Configuration
```yaml
# config/config.yaml
platforms:
  # ... existing platforms ...
  linkedin:
    enabled: true
    max_tokens: 400

posting:
  enabled_platforms:
    - twitter
    - medium
    - youtube
    - linkedin  # ← Add here!
```

### Step 4: Add Credentials
```env
# config/secrets.env
LINKEDIN_ACCESS_TOKEN=your_token_here
```

### Step 5: Use It!
```python
# That's it! No other code changes needed!

from agents.poster_factory import PosterFactory
from agents.base_poster import PostPayload

# Will automatically work!
linkedin_poster = PosterFactory.create("linkedin")
payload = PostPayload(
    platform="linkedin",
    title="",
    content="Check out this article!"
)
result = linkedin_poster.post(payload)

# Or use legacy function
from agents.linkedin_poster import post_to_linkedin
post_to_linkedin("Check out this article!")

# Or with LivePoster - automatically includes LinkedIn
from agents.live_poster import LivePoster
poster = LivePoster()  # Reads enabled_platforms from config
poster.post_all()
```

**That's the power of modular architecture!** Adding a new platform requires NO changes to LivePoster or any existing code.

---

## Common Migration Patterns

### Pattern 1: Enabling/Disabling Platforms
```yaml
# BEFORE: Had to modify code
ALLOWED_PLATFORMS = {"TWITTER", "MEDIUM"}

# AFTER: Just edit config
posting:
  enabled_platforms:
    - twitter
    - medium
    - youtube
    - linkedin
```

### Pattern 2: Changing Models
```yaml
# BEFORE: Hard-coded in code
MODEL_NAME = "gpt2"

# AFTER: Just change config
model:
  name: HuggingFaceH4/zephyr-7b-beta
```

### Pattern 3: Testing Without Posting
```python
# BEFORE: Hard-coded in code
LIVE_MODE = False  # Hope you remember to change this!

# AFTER: Config-driven
posting:
  live_mode: false  # Clear what mode you're in
```

### Pattern 4: Different Configs per Environment
```yaml
# config/config.yaml (shared)
# config/config.prod.yaml (production overrides)
# config/config.test.yaml (test overrides)

from utils.config_loader import ConfigLoader
config = ConfigLoader()  # Loads appropriate config based on ENV
```

---

## Checklist for Migration

- [ ] Update imports to use new classes
- [ ] Pass config to writers/posters explicitly
- [ ] Move hard-coded values to config.yaml
- [ ] Test with new modular approach
- [ ] Keep legacy functions for backward compatibility
- [ ] Update any custom scripts to use new patterns
- [ ] Test error handling with missing credentials
- [ ] Verify logging works as expected

---

## Questions & Troubleshooting

**Q: I still want to use the old way, is that OK?**
A: Yes! All legacy functions are preserved. They internally use the new modular approach.

**Q: How do I test without actually posting?**
A: Set `posting.live_mode: false` in config.yaml or pass `live_mode=False` to LivePoster constructor.

**Q: Can I use different configs for different environments?**
A: Yes! Extend ConfigLoader to support multiple config files or environment-specific overrides.

**Q: What if I need to change behavior for one platform?**
A: Modify only that platform's class. Other platforms are unaffected. That's SRP!

**Q: How do I add logging?**
A: All classes accept optional `logger` parameter. Pass a logger to any class and it will use it.
