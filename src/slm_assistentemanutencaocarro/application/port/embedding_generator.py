from typing import Protocol

from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)


class EmbeddingGenerator(Protocol):
    def embed_query(self, question: str) -> list[float]:
        ...

    def embed_documents(
        self,
        chunks: list[KnowledgeChunk],
    ) -> list[list[float]]:
        ...
