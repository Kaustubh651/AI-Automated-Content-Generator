#agent\youtube_writer.py
from agents.llm_engine import LLMEngine

llm = LLMEngine()

def write_youtube(article):
    prompt = f"""
You are a tech YouTuber.

Write a 60–90 second script.
Rules:
- Strong hook
- Explain impact on industry
- Simple language
- End with call to action (subscribe/comment)

Article:
{article}
"""
    return llm.generate(prompt, max_new_tokens=500)
