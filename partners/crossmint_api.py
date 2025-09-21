import os, aiohttp, json
from typing import Optional

async def call_crossmint(payload: str, api_key: Optional[str]=None) -> str:
    if api_key is None:
        api_key = os.getenv("CROSSMINT_API_KEY")
    if not api_key:
        raise ValueError("CROSSMINT_API_KEY required")
    url = os.getenv("CROSSMINT_API_URL", "https://api.crossmint.io/v1/endpoint")
    headers = {"x-client-secret": api_key, "Content-Type": "application/json"}
    data = {"payload": payload}
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, headers=headers, json=data) as resp:
            text = await resp.text()
            if resp.status != 200:
                raise Exception(f"Crossmint error {resp.status}: {text}")
            return await resp.json()
