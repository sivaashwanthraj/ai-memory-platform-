import httpx
from app.config import settings

try:
    import ollama
except ImportError:
    ollama = None


class LLMService:
    def __init__(self):
        self.model = "qwen3:4b"

    async def generate(self, prompt: str) -> str:
        system_instruction = (
            "You are an AI Memory Assistant.\n"
            "Use ONLY the memories provided.\n"
            "If the answer is not present in the memories, reply exactly:\n"
            '"I don\'t know because it isn\'t in my memory."'
        )

        # 1. Check if Groq Cloud API is configured (Free & Fast for 24/7 cloud)
        if settings.GROQ_API_KEY or settings.LLM_PROVIDER == "groq":
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    res = await client.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "qwen/qwen3.8-27b",
                            "messages": [
                                {"role": "system", "content": system_instruction},
                                {"role": "user", "content": prompt},
                            ],
                            "temperature": 0.2,
                        },
                    )
                    data = res.json()
                    if res.status_code != 200:
                        err_msg = data.get("error", {}).get("message", res.text)
                        return f"Groq API Error ({res.status_code}): {err_msg}"
                    if "choices" in data and len(data["choices"]) > 0:
                        return data["choices"][0]["message"]["content"]
                    return "No response generated from LLM."
            except Exception as e:
                return f"Groq LLM Error: {str(e)}"

        # 2. Check if OpenAI Cloud API is configured
        if settings.OPENAI_API_KEY or settings.LLM_PROVIDER == "openai":
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    res = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "gpt-4o-mini",
                            "messages": [
                                {"role": "system", "content": system_instruction},
                                {"role": "user", "content": prompt},
                            ],
                            "temperature": 0.2,
                        },
                    )
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
            except Exception as e:
                return f"OpenAI LLM Error: {str(e)}"

        # 3. Default to local Ollama
        try:
            if ollama is None:
                return "Ollama is not installed or not available in this environment."
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
            )
            return response["message"]["content"]
        except Exception as e:
            return f"LLM Error: {str(e)}"