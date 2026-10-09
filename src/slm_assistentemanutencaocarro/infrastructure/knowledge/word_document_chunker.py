from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_document import (
    KnowledgeDocument,
)


class WordDocumentChunker:
    def __init__(
        self,
        chunk_size: int = 120,
        overlap: int = 20,
    ):
        if chunk_size < 1:
            raise ValueError("chunk_size deve ser maior que zero.")

        if overlap < 0 or overlap >= chunk_size:
            raise ValueError(
                "overlap deve ser maior ou igual a zero "
                "e menor que chunk_size."
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(
        self,
        document: KnowledgeDocument,
    ) -> list[KnowledgeChunk]:
        words = document.content.split()
        chunks: list[KnowledgeChunk] = []
        step = self.chunk_size - self.overlap

        for start in range(0, len(words), step):
            position = len(chunks)

            chunks.append(
                KnowledgeChunk(
                    id=f"{document.id}:chunk:{position}",
                    document_id=document.id,
                    title=document.title,
                    content=" ".join(
                        words[start : start + self.chunk_size]
                    ),
                    source=document.source,
                    position=position,
                    vehicle_id=document.vehicle_id,
                )
            )

            if start + self.chunk_size >= len(words):
                break

        return chunks
