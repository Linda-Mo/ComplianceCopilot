import os
import aiohttp
import json
from typing import Optional

async def call_nebius(prompt: str, api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> str:
    """
    Nebius AI Studio helper — expects Bearer token in NEBIUS_API_KEY.
    Update url/payload parsing if Nebius docs differ.
    """
    if api_key is None:
        api_key = os.getenv("NEBIUS_API_KEY")
    if not api_key:
        raise ValueError("NEBIUS_API_KEY is required")

    url = os.getenv("NEBIUS_API_URL", "https://api.nebius.ai/v1/generate")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "prompt": prompt, "max_tokens": int(os.getenv("NEBIUS_MAX_TOKENS", "512"))}

    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            text = await resp.text()
            if resp.status != 200:
                raise Exception(f"Nebius API error: {resp.status} - {text}")
            data = await resp.json()
            # Adapt parsing to Nebius response shape:
            if isinstance(data, dict):
                if "output" in data:
                    return data["output"]
                if "choices" in data and data["choices"]:
                    return data["choices"][0].get("text") or json.dumps(data["choices"][0])
            return json.dumps(data)
