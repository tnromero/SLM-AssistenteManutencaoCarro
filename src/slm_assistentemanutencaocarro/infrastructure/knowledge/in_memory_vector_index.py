from math import hypot, isfinite

from slm_assistentemanutencaocarro.application.model.embedded_chunk import (
    EmbeddedChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (  # noqa: E501
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.port.vector_index import (
    VectorIndex,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class InMemoryVectorIndex(VectorIndex):

    def __init__(self):
        self._entries: tuple[EmbeddedChunk, ...] = ()
        self._dimension: int | None = None
        self._ready = False

    def replace(self, entries: list[EmbeddedChunk]) -> None:
        dimension = len(entries[0].vector) if entries else None
        known_ids: set[str] = set()

        for entry in entries:
            self._validate_vector(entry.vector)

            if len(entry.vector) != dimension:
                raise ValueError("Dimensões inconsistentes.")

            if entry.chunk.id in known_ids:
                raise ValueError("Identidade de chunk duplicada.")

            known_ids.add(entry.chunk.id)

        # Substitui somente após validar todo o novo conteúdo.
        self._entries = tuple(entries)
        self._dimension = dimension
        self._ready = True

    def search(
        self,
        query_vector: list[float],
        vehicle_id: VehicleId | None,
        top_k: int = 3,
    ) -> list[KnowledgeSearchResult]:
        if top_k < 1:
            raise ValueError("top_k deve ser maior que zero.")

        query_norm = self._validate_vector(query_vector)

        if not self._entries:
            return []

        if len(query_vector) != self._dimension:
            raise ValueError("Dimensão da pergunta incompatível com o índice.")

        results = []

        for entry in self._entries:
            if (
                entry.chunk.vehicle_id is not None
                and entry.chunk.vehicle_id != vehicle_id
            ):
                continue

            document_norm = self._validate_vector(entry.vector)

            score = sum(
                (query_value / query_norm)
                * (document_value / document_norm)
                for query_value, document_value in zip(
                    query_vector,
                    entry.vector,
                    strict=True,
                )
            )

            results.append(
                KnowledgeSearchResult(
                    chunk=entry.chunk,
                    score=score,
                )
            )

        return sorted(
            results,
            key=lambda result: result.score,
            reverse=True,
        )[:top_k]

    @staticmethod
    def _validate_vector(vector: list[float] | tuple[float, ...]) -> float:
        if not vector or not all(isfinite(value) for value in vector):
            raise ValueError("O vetor deve conter valores finitos.")

        norm = hypot(*vector)

        if norm == 0 or not isfinite(norm):
            raise ValueError("O vetor deve ter norma finita e maior que zero.")

        return norm

    def is_ready(self) -> bool:
        return self._ready

    def count(self) -> int:
        return len(self._entries)
