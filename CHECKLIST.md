# Project Checklist — Environment & Run Steps

## Required Python packages
Install the dependencies listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Recommended core packages (if installing selectively):
```bash
pip install torch transformers newspaper3k beautifulsoup4 pandas numpy schedule tweepy moviepy sentence-transformers google-api-python-client google-auth-oauthlib google-auth-httplib2 lxml pyyaml playwright pillow
```

Playwright note: after installing, run:
```bash
playwright install
```

## Required environment variables / secrets
Set these (example names) in `config/secrets.env` or your environment:

- TWITTER_API_KEY
- TWITTER_API_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_SECRET
- MEDIUM_API_TOKEN (optional)
- GOOGLE_OAUTH_CLIENT_ID / CLIENT_SECRET (for YouTube upload)

Also ensure `config/config.yaml` has the correct `posting` config:
- `posting.queue_dir` (default: `data/post_queue`)
- `posting.enabled_platforms` (e.g., `["twitter","medium","youtube"]`)
- `mode` or `live` flag used by `shared.config.ConfigLoader` to determine `is_live_mode()`

## Quick run commands
Run import checks:
```bash
python -c "from services import generate_content, scrape_news; print('imports ok')"
```

Run the daily pipeline (generates content locally):
```bash
python pipelines/daily_run.py
```

Run the trend-driven pipeline (full flow, will queue payloads):
```bash
python pipelines/trend_driven_run.py
```

Dry-run posting (safe preview mode — no network posting):
```bash
python -c "from services.post_router import LivePoster; LivePoster(live_mode=False).post_all()"
```

Run the dry-run test script I added:
```bash
python tests/dry_run_liveposter.py
```

## Notes & Caveats
- Some sites return HTTP 403 to scraping tools (e.g., `newspaper3k`); this is external and may require custom scraping headers or a different scraper.
- Full posting requires valid API keys and correct `live_mode` configuration; otherwise posters either save drafts or raise missing-credentials errors.
- For Playwright (Instagram automation) ensure a GUI or set up proper headless browser credentials and sessions.

## Troubleshooting
- If an import fails, re-check `PYTHONPATH` and that you're running from the repository root:
```bash
cd /path/to/PROJECT-AUTOMATE
python -c "from services import generate_content; print('ok')"
```
- If `tweepy` functions fail, update to the latest `tweepy` from pip and confirm environment variables.

## Next recommended steps
- Add unit tests for writers and posters.
- Add integration test to run pipelines with a mocked LLM or a stub `LLMEngine`.
- Add CI job that installs dependencies and runs the smoke tests.
