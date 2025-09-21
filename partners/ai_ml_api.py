import os, aiohttp, json
from typing import Optional

async def call_ai_ml(prompt: str, api_key: Optional[str]=None) -> str:
    if api_key is None:
        api_key = os.getenv("AI_ML_API_KEY")
    if not api_key:
        raise ValueError("AI_ML_API_KEY required")
    url = os.getenv("AI_ML_API_URL", "https://api.example-aiml.com/v1/complete")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"input": prompt, "max_tokens": 512}
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            text = await resp.text()
            if resp.status != 200:
                raise Exception(f"AI/ML API error {resp.status}: {text}")
            data = await resp.json()
            if isinstance(data, dict):
                if "result" in data:
                    return data["result"]
                if "choices" in data and data["choices"]:
                    return data["choices"][0].get("text") or json.dumps(data["choices"][0])
            return json.dumps(data)

async def run_model(data: dict):
    return {"status": "simulated", "result": "AI/ML placeholder result"}
