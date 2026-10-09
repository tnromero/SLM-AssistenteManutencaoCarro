import os


class Settings:
    ollama_intent_model: str = os.getenv(
        "OLLAMA_INTENT_MODEL", 
        "qwen3:1.7b"
    )
    ollama_question_model: str = os.getenv(
        "OLLAMA_QUESTION_MODEL", 
        "qwen3:1.7b"
    )
    ollama_response_model: str = os.getenv(
        "OLLAMA_RESPONSE_MODEL", 
        "qwen3:1.7b"
    )
    ollama_resolver_model: str = os.getenv(
        "OLLAMA_RESOLVER_MODEL",
        "qwen3:1.7b",
    )
    session_file: str = os.getenv(
        "SESSION_FILE",
        "data/session.json",
    )
    knowledge_manifest_file: str = os.getenv(
        "KNOWLEDGE_MANIFEST_FILE",
        "data/knowledge/manifest.json",
    )
