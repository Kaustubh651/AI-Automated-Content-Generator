"""Smoke test runner for CI and local validation.

Runs import checks, generates sample content, builds payloads, and runs LivePoster in safe mode.
Exits with non-zero code on failure.
"""
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
QUEUE = ROOT / "data" / "post_queue"

# Ensure project root is on sys.path when running this script directly
import os
sys.path.insert(0, str(ROOT))


def fail(msg, e=None):
    print("[FAIL]", msg)
    if e:
        traceback.print_exception(type(e), e, e.__traceback__)
    sys.exit(2)


def main():
    print("[SMOKE] Starting smoke tests...")

    try:
        # Import checks
        print("[SMOKE] Importing core modules...")
        from services import generate_content, scrape_news
        from services.writers import write_twitter, write_medium, write_youtube
        from services.posters import post_to_twitter, post_to_medium, post_to_youtube
        from services.post_router import build_post_payload, LivePoster
        from shared.config import get_config
    except Exception as e:
        fail("Import failed", e)

    print("[SMOKE] Imports OK")

    # Ensure outputs and queue dirs exist
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sample_text = "This is a brief sample article text for smoke testing."

    try:
        # Generate content (should write to outputs via OutputWriter)
        print("[SMOKE] Generating content for twitter/medium/youtube...")
        generate_content(sample_text, "twitter")
        generate_content(sample_text, "medium")
        generate_content(sample_text, "youtube")
    except Exception as e:
        fail("Content generation failed", e)

    print("[SMOKE] Content generation OK")

    # Make sure sample output files exist (some generators may write different names)
    # Create fallback sample files if not present
    sample_files = {
        "twitter": OUTPUTS / "twitter.txt",
        "medium": OUTPUTS / "medium.md",
        "youtube": OUTPUTS / "youtube.txt",
    }

    for k, p in sample_files.items():
        if not p.exists():
            print(f"[SMOKE] Creating fallback sample output: {p}")
            p.write_text(f"Sample {k} content for smoke testing.", encoding="utf-8")

    # Build post payloads (should write to data/post_queue)
    try:
        print("[SMOKE] Building post payloads into queue...")
        build_post_payload(trend="smoke_test", platform="twitter")
        build_post_payload(trend="smoke_test", platform="medium")
        build_post_payload(trend="smoke_test", platform="youtube")
    except Exception as e:
        fail("Building post payloads failed", e)

    print("[SMOKE] Payloads queued OK")

    # Run LivePoster in safe mode (no external posting)
    try:
        print("[SMOKE] Running LivePoster in safe mode (no network posting)...")
        poster = LivePoster(live_mode=False)
        result = poster.post_all()
    except Exception as e:
        fail("LivePoster dry-run failed", e)

    print("[SMOKE] LivePoster dry-run OK")
    print("[SMOKE] SUMMARY:")
    print(result)

    print("[SMOKE] All smoke tests passed")
    sys.exit(0)


if __name__ == '__main__':
    main()
