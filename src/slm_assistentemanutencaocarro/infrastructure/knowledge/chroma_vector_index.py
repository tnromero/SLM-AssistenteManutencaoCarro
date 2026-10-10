from math import hypot, isfinite

from chromadb.api.models.Collection import Collection
from chromadb.api.types import Where

from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.knowledge.chroma_chunk_mapper import (
    deserialize_chunk,
)


class ChromaVectorIndex:
    def __init__(self, collection: Collection):
        self._collection = collection

    def search(
        self,
        query_vector: list[float],
        vehicle_id: VehicleId | None,
        top_k: int = 3,
    ) -> list[KnowledgeSearchResult]:
        if top_k < 1:
            raise ValueError("top_k deve ser maior que zero.")

        if not query_vector or not all(
            isfinite(value) for value in query_vector
        ):
            raise ValueError("O vetor deve conter valores finitos.")

        norm = hypot(*query_vector)

        if norm == 0 or not isfinite(norm):
            raise ValueError("O vetor deve ter norma finita e maior que zero.")

        where = self._vehicle_filter(vehicle_id)

        eligible = self._collection.get(
            where=where,
            include=[],
        )
        eligible_count = len(eligible["ids"])

        if eligible_count == 0:
            return []

        response = self._collection.query(
            query_embeddings=[query_vector],
            where=where,
            n_results=min(top_k, eligible_count),
            include=["documents", "metadatas", "distances"],
        )

        documents = response["documents"]
        metadatas = response["metadatas"]
        distances = response["distances"]

        if (
            documents is None
            or metadatas is None
            or distances is None
        ):
            raise ValueError("O Chroma retornou resultados incompletos.")

        results = []

        for chunk_id, content, metadata, distance in zip(
            response["ids"][0],
            documents[0],
            metadatas[0],
            distances[0],
            strict=True,
        ):
            if content is None or metadata is None:
                raise ValueError("O registro não contém texto ou metadados.")

            results.append(
                KnowledgeSearchResult(
                    chunk=deserialize_chunk(
                        chunk_id=chunk_id,
                        content=content,
                        metadata=dict(metadata),
                    ),
                    score=1.0 - distance,
                )
            )

        return results

    @staticmethod
    def _vehicle_filter(vehicle_id: VehicleId | None) -> Where:
        if vehicle_id is None:
            return {"is_general": True}

        return {
            "$or": [
                {"is_general": True},
                {
                    "$and": [
                        {"is_general": False},
                        {"vehicle_id": vehicle_id.value},
                    ]
                },
            ]
        }
