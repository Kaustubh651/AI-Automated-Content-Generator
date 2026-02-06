#agent\medium_writer.py
from agents.llm_engine import LLMEngine

llm = LLMEngine()

def write_medium(article):
    prompt = f"""
You are a tech blogger writing for Medium.

Write a thoughtful article based on the news.
Structure:
- Title
- Short intro
- 3 sections with headings
- Practical conclusion

Tone: analytical, clear, human.

Article:
{article}
"""
    return llm.generate(prompt, max_new_tokens=600)
