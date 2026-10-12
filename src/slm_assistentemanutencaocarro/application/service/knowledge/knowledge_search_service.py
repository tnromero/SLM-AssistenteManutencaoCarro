from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.exception import (
    KnowledgeIndexNotReadyError,
)
from slm_assistentemanutencaocarro.application.model.knowledge.embedded_chunk import (  # noqa: E501
    EmbeddedChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge.knowledge_search_result import (  # noqa: E501
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.port.knowledge.document_chunker import (  # noqa: E501
    DocumentChunker,
)
from slm_assistentemanutencaocarro.application.port.knowledge.embedding_generator import (  # noqa: E501
    EmbeddingGenerator,
)
from slm_assistentemanutencaocarro.application.port.knowledge.knowledge_reader import (  # noqa: E501
    KnowledgeReader,
)
from slm_assistentemanutencaocarro.application.port.knowledge.vector_index import (  # noqa: E501
    VectorIndex,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class KnowledgeSearchService:
    
    def __init__(
        self,
        knowledge_reader: KnowledgeReader,
        chunker: DocumentChunker,
        embedding_generator: EmbeddingGenerator,
        vector_index: VectorIndex,
        vehicle_context: VehicleContext,
    ):
        self.knowledge_reader = knowledge_reader
        self.chunker = chunker
        self.embedding_generator = embedding_generator
        self.vector_index = vector_index
        self.vehicle_context = vehicle_context

    def build_index(self) -> int:
        chunks = [
            chunk
            for document in self.knowledge_reader.list_documents()
            for chunk in self.chunker.split(document)
        ]

        entries: list[EmbeddedChunk] = []

        if chunks:
            vectors = self.embedding_generator.embed_documents(chunks)

            entries = [
                EmbeddedChunk(
                    chunk=chunk,
                    vector=tuple(vector),
                )
                for chunk, vector in zip(chunks, vectors, strict=True)
            ]

        self.vector_index.replace(entries)

        return len(entries)

    def search(
        self,
        question: str,
        top_k: int = 3,
        *,
        vehicle_id: VehicleId | None = None,
    ) -> list[KnowledgeSearchResult]:
        if not question.strip():
            raise ValueError("A pergunta não pode ser vazia.")

        if top_k < 1:
            raise ValueError("top_k deve ser maior que zero.")

        if not self.vector_index.is_ready():
            raise KnowledgeIndexNotReadyError(
                "A base de conhecimento ainda não foi indexada."
            )

        if self.vector_index.count() == 0:
            return []

        query_vector = self.embedding_generator.embed_query(question)

        return self.vector_index.search(
            query_vector=query_vector,
            vehicle_id=(
                vehicle_id
                if vehicle_id is not None
                else self.vehicle_context.get_selected()
            ),
            top_k=top_k,
        )
