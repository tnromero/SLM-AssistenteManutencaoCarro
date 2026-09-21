import os


class Settings:
    ollama_intent_model: str = os.getenv("OLLAMA_INTENT_MODEL", "qwen3:1.7b")
    ollama_question_model: str = os.getenv("OLLAMA_QUESTION_MODEL", "qwen3:1.7b")
    ollama_response_model: str = os.getenv("OLLAMA_RESPONSE_MODEL", "qwen3:1.7b")
