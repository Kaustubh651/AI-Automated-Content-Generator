import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.llm_engine import LLMEngine

try:
    llm = LLMEngine()
    
    prompt = """
Explain why AI agents are becoming more important than chatbots.
Give a strong opinion.
"""
    
    result = llm.generate(prompt)
    print(result)
except Exception as e:
    print(f"Test failed with error: {e}")
    import traceback
    traceback.print_exc()
