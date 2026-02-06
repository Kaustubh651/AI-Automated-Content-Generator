import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from agents.trend_bias_engine import apply_trend_bias

print(apply_trend_bias("AI agents are evolving fast.", "RISING"))
