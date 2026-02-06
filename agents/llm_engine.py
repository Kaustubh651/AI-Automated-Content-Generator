# agent\llm_engine.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Using gpt2 instead of gemma-2b-it for better compatibility (no authentication needed)
MODEL_NAME = "gpt2"

class LLMEngine:
    def __init__(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            ).to(self.device)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def generate(self, prompt, max_new_tokens=300):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
