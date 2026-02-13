"""Platform-level posting orchestrator."""

def post_to_platform(payload, safe_mode=True):
    platform = payload["platform"]

    print(f"\n[SPRINT 6B] 🚀 Preparing post for {platform.upper()}")

    if safe_mode:
        print("[SAFE MODE] No real posting executed")
        print("--------- POST PREVIEW ---------")
        print(payload["content"][:300])
        print("--------------------------------")
        return

    # LIVE MODE (Sprint 6C+)
    if platform == "twitter":
        post_twitter(payload)
    elif platform == "medium":
        post_medium(payload)
    elif platform == "youtube":
        post_youtube(payload)
    elif platform == "instagram":
        post_instagram(payload)

