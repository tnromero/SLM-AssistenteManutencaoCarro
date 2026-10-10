from math import hypot, isfinite
from uuid import uuid4

from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection
from chromadb.api.types import Where

from slm_assistentemanutencaocarro.application.model.embedded_chunk import (
    EmbeddedChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (  # noqa: E501
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.knowledge.chroma_chunk_mapper import (  # noqa: E501
    deserialize_chunk,
    serialize_metadata,
)


class ChromaVectorIndex:
    
    def __init__(
        self,
        client: ClientAPI,
        collection_name: str,
        embedding_model: str,
    ):
        self._client = client
        self._collection_name = collection_name
        self._embedding_model = embedding_model

        self._registry = client.get_or_create_collection(
            name=f"{collection_name}-registry",
            embedding_function=None,
            metadata={"active_collection": ""},
        )

        metadata = self._registry.metadata or {}
        active_name = metadata.get("active_collection", "")

        if not isinstance(active_name, str):
            raise ValueError("Referência do índice ativo inválida.")

        self._collection: Collection | None = None

        if active_name:
            if metadata.get("embedding_model") != embedding_model:
                raise ValueError(
                    "O índice foi criado com outro modelo de embeddings. "
                    "Use uma coleção lógica diferente para o novo modelo."
                )

            self._collection = client.get_collection(
                name=active_name,
                embedding_function=None,
            )

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

        collection = self._collection

        if collection is None:
            return []

        eligible = collection.get(
            where=where,
            include=[],
        )
        eligible_count = len(eligible["ids"])

        if eligible_count == 0:
            return []

        response = collection.query(
            query_embeddings=[query_vector],
            where=where,
            n_results=min(top_k, eligible_count),
            include=["documents", "metadatas", "distances"],
        )

        documents = response["documents"]
        metadatas = response["metadatas"]
        distances = response["distances"]

        if documents is None or metadatas is None or distances is None:
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

    def replace(self, entries: list[EmbeddedChunk]) -> None:
        dimension = len(entries[0].vector) if entries else 0
        known_ids: set[str] = set()
        metadatas = []

        for entry in entries:
            vector = entry.vector

            if not vector or not all(isfinite(value) for value in vector):
                raise ValueError("Embedding inválido.")

            norm = hypot(*vector)

            if norm == 0 or not isfinite(norm):
                raise ValueError("Embedding com norma inválida.")

            if len(vector) != dimension:
                raise ValueError("Dimensões inconsistentes.")

            if entry.chunk.id in known_ids:
                raise ValueError("Identidade de chunk duplicada.")

            known_ids.add(entry.chunk.id)
            metadatas.append(serialize_metadata(entry.chunk))

        candidate = self._client.create_collection(
            name=f"{self._collection_name}-{uuid4().hex}",
            embedding_function=None,
            configuration={"hnsw": {"space": "cosine"}},
        )

        batch_size = self._client.get_max_batch_size()

        for start in range(0, len(entries), batch_size):
            batch = entries[start : start + batch_size]

            candidate.add(
                ids=[entry.chunk.id for entry in batch],
                documents=[entry.chunk.content for entry in batch],
                embeddings=[list(entry.vector) for entry in batch],
                metadatas=metadatas[start : start + batch_size],
            )

        if candidate.count() != len(entries):
            raise ValueError("A gravação do novo índice ficou incompleta.")

        self._registry.modify(
            metadata={
                "active_collection": candidate.name,
                "embedding_model": self._embedding_model,
                "dimension": dimension,
            }
        )

        self._collection = candidate
