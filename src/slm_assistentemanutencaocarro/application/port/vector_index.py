from typing import Protocol

from slm_assistentemanutencaocarro.application.model.embedded_chunk import (
    EmbeddedChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class VectorIndex(Protocol):
    def replace(self, entries: list[EmbeddedChunk]) -> None:
        ...

    def search(
        self,
        query_vector: list[float],
        vehicle_id: VehicleId | None,
        top_k: int = 3,
    ) -> list[KnowledgeSearchResult]:
        ...
