from app.ai.providers.groq import GroqProvider
from app.ai.providers.ollama import OllamaProvider
from app.ai.providers.vllm import VLLMProvider


def get_provider(name: str):

    providers = {
        "groq": GroqProvider,
        "ollama": OllamaProvider,
        "vllm": VLLMProvider,
    }

    provider_class = providers.get(name.lower())

    if not provider_class:
        raise ValueError(
            f"Unsupported AI provider: {name}"
        )

    return provider_class()