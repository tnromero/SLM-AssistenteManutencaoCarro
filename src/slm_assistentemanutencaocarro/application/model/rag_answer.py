from dataclasses import dataclass

from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (
    KnowledgeSearchResult,
)


@dataclass(frozen=True)
class RagAnswer:
    response: str
    results: tuple[KnowledgeSearchResult, ...]
