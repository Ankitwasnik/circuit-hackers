import os
from src.llm.openai import OpenAILLM
from src.llm.llm_interface import LLMInterface
from src.llm.llm_providers import LLMProviders


class LLMProvider:
    @staticmethod
    def get_chat_model():
        """Get the chat LLM model based on the provider."""
        return _LLMFactory.get_provider().get_chat_model()

    @staticmethod
    def get_embedding_model():
        """Get the embedding LLM model based on the provider."""
        return _LLMFactory.get_provider().get_embedding_model()


class _LLMFactory:
    providers = {
        LLMProviders.OPENAI.value: OpenAILLM,
    }

    @staticmethod
    def get_provider() -> LLMInterface:
        provider = os.getenv("LLM_PROVIDER")
        if provider not in _LLMFactory.providers:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        return _LLMFactory.providers[provider]()
