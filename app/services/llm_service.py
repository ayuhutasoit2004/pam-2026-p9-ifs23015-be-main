import requests
from app.config import Config

def generate_from_llm(prompt: str):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {Config.LLM_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    if response.status_code != 200:
        raise Exception(f"LLM request failed: {response.text}")

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return {"response": content}