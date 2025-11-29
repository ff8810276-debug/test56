from fastapi import FastAPI
from llama_cpp import Llama
import json
import re

app = FastAPI()

llm = Llama(
    model_path="model.gguf",
    n_ctx=2048
)

def extract_json(text):
    # پیدا کردن اولین { و آخرین }
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None

@app.get("/skills")
def get_skills(role: str):
    prompt = f"""
You MUST return ONLY valid JSON.

Task: Generate EXACTLY 10 core skills for the role "{role}".

JSON format:
{{
  "role": "{role}",
  "skills": [
    "skill1",
    "skill2",
    ...
    "skill10"
  ]
}}
"""

    output = llm(prompt, max_tokens=600)
    text = output["choices"][0]["text"]

    json_data = extract_json(text)

    if json_data:
        return json_data
    
    return {
        "error": "Model output not valid JSON",
        "raw_output": text
    }
