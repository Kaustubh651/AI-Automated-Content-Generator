from agents.llm_engine import LLMEngine

llm = LLMEngine()

def write_twitter(article):
    prompt = f"""
You are a tech founder on X.

Read the article below and write a sharp opinion thread.
Rules:
- Confident tone
- Slightly controversial
- 5–7 tweets
- No emojis
- Hook in first line

Article:
{article}
"""
    return llm.generate(prompt, max_new_tokens=250)
