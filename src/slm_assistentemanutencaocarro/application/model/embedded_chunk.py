from dataclasses import dataclass

from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)


@dataclass(frozen=True)
class EmbeddedChunk:
    chunk: KnowledgeChunk
    vector: tuple[float, ...]
