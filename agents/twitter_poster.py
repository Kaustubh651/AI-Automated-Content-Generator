import os
import tweepy
from dotenv import load_dotenv

# Load secrets
load_dotenv("config/secrets.env")

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")


def post_to_twitter(text: str):
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
        raise EnvironmentError("❌ Twitter API credentials missing")

    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )

    response = client.create_tweet(text=text[:280])
    print(f"[TWITTER] ✅ Tweet posted | id={response.data['id']}")
