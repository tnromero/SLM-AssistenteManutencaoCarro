from dataclasses import dataclass


@dataclass(frozen=True)
class RagRetrievedPassage:
    citation_id: int
    chunk_id: str
    document_id: str
    title: str
    content: str
    source: str
    score: float