from fastapi import FastAPI
from llama_cpp import Llama

app = FastAPI()

llm = Llama(
    model_path="qwen2.5-1.5b-q4_k_m.gguf",
    n_ctx=2048
)

@app.get("/skills")
def get_skills(role: str):
    prompt = f"""
Role: {role}
Return exactly 10 skills.
Output JSON only:
{{
  "role": "{role}",
  "skills": []
}}
"""
    output = llm(prompt, max_tokens=512)
    return output["choices"][0]["text"]
