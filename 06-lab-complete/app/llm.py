import json
import urllib.request
import urllib.error
import logging
from app.config import settings
from utils.mock_llm import ask as mock_ask

logger = logging.getLogger(__name__)

def ask(question: str) -> str:
    """
    Hàm gọi LLM đa năng:
    1. Nếu có OLLAMA_BASE_URL: Gọi API của Ollama cục bộ/cloud.
    2. Nếu có OPENAI_API_KEY: Gọi API OpenAI.
    3. Nếu không có gì: Tự động fallback về Mock LLM.
    """
    # 1. Sử dụng Ollama (Qwen/Llama...)
    if settings.ollama_base_url:
        try:
            logger.info(f"Routing request to Ollama: {settings.ollama_base_url} (Model: {settings.ollama_model})")
            url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"
            data = {
                "model": settings.ollama_model,
                "messages": [{"role": "user", "content": question}],
                "stream": False
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                res = json.loads(response.read().decode("utf-8"))
                return res["message"]["content"]
        except urllib.error.URLError as e:
            logger.error(f"Ollama connection error: {e}. Falling back to Mock LLM.")
            return f"[Ollama Connection Error: {e}] " + mock_ask(question)
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}. Falling back to Mock LLM.")
            return f"[Ollama Error: {str(e)[:100]}] " + mock_ask(question)

    # 2. Sử dụng OpenAI
    if settings.openai_api_key:
        try:
            logger.info(f"Routing request to OpenAI (Model: {settings.llm_model})")
            url = "https://api.openai.com/v1/chat/completions"
            data = {
                "model": settings.llm_model,
                "messages": [{"role": "user", "content": question}],
                "temperature": 0.7
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.openai_api_key}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                res = json.loads(response.read().decode("utf-8"))
                return res["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error calling OpenAI: {e}. Falling back to Mock LLM.")
            return f"[OpenAI Error: {str(e)[:100]}] " + mock_ask(question)

    # 3. Sử dụng Mock LLM
    logger.info("No LLM keys configured — using Mock LLM")
    return mock_ask(question)
