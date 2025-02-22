from abc import ABC, abstractmethod


# Base Interface
class LLMInterface(ABC):
    @abstractmethod
    def get_chat_model(self):
        """Get chat LLM model."""
        pass

    @abstractmethod
    def get_embedding_model(self):
        """Get embedding LLM model."""
        pass
