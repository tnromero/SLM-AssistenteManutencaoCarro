import hashlib
import json


def build_index_signature(
    embedding_model: str,
    chunk_size: int,
    overlap: int,
) -> str:
    configuration = {
        "embedding_model": embedding_model,
        "embedding_format": "embeddinggemma-search-v1",
        "chunker": "word-v1",
        "chunk_size": chunk_size,
        "overlap": overlap,
        "metadata_schema": "chunk-v1",
        "distance": "cosine",
    }

    content = json.dumps(
        configuration,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(content.encode("utf-8")).hexdigest()
