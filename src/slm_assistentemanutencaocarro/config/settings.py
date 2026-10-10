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
    ollama_embedding_model: str = os.getenv(
        "OLLAMA_EMBEDDING_MODEL",
        "embeddinggemma:300m",
    )
    ollama_rag_model: str = os.getenv(
        "OLLAMA_RAG_MODEL",
        "qwen3:1.7b",
    )
    vector_db_path: str = os.getenv(
        "VECTOR_DB_PATH",
        "data/vector_db",
    )
    vector_collection_name: str = os.getenv(
        "VECTOR_COLLECTION_NAME",
        "vehicle-knowledge-v2",
    )
    