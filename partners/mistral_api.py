import os, aiohttp, json
from typing import Optional

async def call_mistral(prompt: str, api_key: Optional[str]=None, model: str="mistral-large") -> str:
    if api_key is None:
        api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY required")
    url = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai/v1/generate")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "input": prompt}
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            text = await resp.text()
            if resp.status != 200:
                raise Exception(f"Mistral error {resp.status}: {text}")
            data = await resp.json()
            # adapt accordingly:
            if isinstance(data, dict):
                if "output" in data:
                    return data["output"]
                if "generations" in data and data["generations"]:
                    return data["generations"][0].get("text") or json.dumps(data["generations"][0])
            return json.dumps(data)

async def analyze_text(text: str):
    return {"status": "simulated", "summary": f"Simulated analysis of: {text[:50]}..."}
