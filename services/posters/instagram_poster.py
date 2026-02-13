"""Instagram poster. Handles automated posting via browser automation."""

from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_DIR = Path("sessions/instagram")
SESSION_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = SESSION_DIR / "state.json"


def post_to_instagram(media_path, caption):
    media_path = Path(media_path)

    if not media_path.exists():
        print(f"[INSTAGRAM] ❌ Media not found: {media_path}")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Session handling
        if STATE_FILE.exists():
            print("[INSTAGRAM] 🔁 Using saved session")
            context = browser.new_context(storage_state=str(STATE_FILE))
        else:
            print("[INSTAGRAM] 🔐 First-time login required")
            context = browser.new_context()

        page = context.new_page()
        page.goto("https://www.instagram.com/", timeout=60000)

        # First login save
        if not STATE_FILE.exists():
            print("👉 Please login manually")
            input("Press ENTER after login is complete...")
            context.storage_state(path=str(STATE_FILE))
            print("[INSTAGRAM] 💾 Session saved")

        print("[INSTAGRAM] ➕ Creating post")

        # Click Create (+)
        page.click("svg[aria-label='New post']", timeout=30000)

        # Upload image
        file_input = page.locator("input[type='file']")
        file_input.set_input_files(str(media_path.resolve()))

        # Next
        page.click("text=Next")
        page.wait_for_timeout(1500)
        page.click("text=Next")

        # Caption
        caption_box = page.locator("div[role='textbox']")
        caption_box.fill(caption)

        # Share
        page.click("text=Share")

        page.wait_for_timeout(5000)

        print("✅ [INSTAGRAM] Post published successfully")
        browser.close()

