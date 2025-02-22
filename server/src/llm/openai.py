import os
from src.llm.llm_interface import LLMInterface


class OpenAILLM(LLMInterface):
    def get_chat_model(self):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            temperature=0, model=os.getenv("OPENAI_CHAT_MODEL_NAME"), verbose=True
        )

    def get_embedding_model(self):
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL_NAME"))
