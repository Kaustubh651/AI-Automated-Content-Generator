import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.instagram_poster import post_to_instagram

post_to_instagram(
    media_path="media/test.png",
    caption="🚀 Automated post from PROJECT-AUTOMATE #AI #Automation"
)
