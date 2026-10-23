"""Shared setup for the smolagents practice scripts."""

import os
import json
from urllib.error import URLError
from urllib.request import urlopen

from dotenv import load_dotenv
from smolagents import InferenceClientModel, OpenAIModel


def make_model(*, vision=False):
    load_dotenv()
    provider = os.getenv("MODEL_PROVIDER", "ollama").strip().lower()
    if provider == "ollama":
        model_key = "OLLAMA_VISION_MODEL" if vision else "OLLAMA_MODEL"
        model_id = os.getenv(model_key, "").strip()
        if vision and not model_id:
            raise SystemExit("Vision lesson အတွက် OLLAMA_VISION_MODEL ထည့်ပါ။")
        model_id = model_id or "qwen3:4b"
        base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1").rstrip("/")
        try:
            with urlopen(base_url.removesuffix("/v1") + "/api/tags", timeout=3) as response:
                installed = {item["name"] for item in json.load(response).get("models", [])}
        except (URLError, TimeoutError, OSError) as exc:
            raise SystemExit("Ollama server မရပါ။ Ollama app ကို ဖွင့်ပြီး ပြန်စမ်းပါ။") from exc
        if model_id not in installed:
            raise SystemExit(f"Local model မရှိသေးပါ။ Run: ollama pull {model_id}")
        return OpenAIModel(model_id=model_id, api_base=base_url, api_key="ollama")

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise SystemExit(
                "GEMINI_API_KEY မတွေ့ပါ။ Google AI Studio မှ API key ထည့်ပါ။"
            )
        model_key = "GEMINI_VISION_MODEL" if vision else "GEMINI_MODEL"
        model_id = os.getenv(model_key, "").strip() or "gemini-2.5-flash"
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        return OpenAIModel(
            model_id=model_id,
            api_base=base_url,
            api_key=api_key,
        )

    if provider != "hf":
        raise SystemExit("MODEL_PROVIDER ကို ollama, gemini သို့မဟုတ် hf လို့ သတ်မှတ်ပါ။")

    token = os.getenv("HF_TOKEN", "").strip()
    if not token or token == "hf_replace_this_with_your_token":
        raise SystemExit(
            "HF_TOKEN မတွေ့ပါ။ .env.example ကို .env အဖြစ် copy လုပ်ပြီး "
            "Hugging Face token ထည့်ပါ။"
        )

    model_key = "HF_VISION_MODEL" if vision else "HF_MODEL"
    model_id = os.getenv(model_key, "").strip()
    if vision and not model_id:
        raise SystemExit("Vision lesson အတွက် .env ထဲမှာ HF_VISION_MODEL ထည့်ပါ။")
    if not vision and not model_id:
        model_id = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

    options = {"token": token}
    if model_id:
        options["model_id"] = model_id
    return InferenceClientModel(**options)
