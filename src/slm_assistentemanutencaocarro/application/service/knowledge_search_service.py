from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.exception import (
    KnowledgeIndexNotReadyError,
)
from slm_assistentemanutencaocarro.application.model.embedded_chunk import (
    EmbeddedChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (  # noqa: E501
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.port.document_chunker import (
    DocumentChunker,
)
from slm_assistentemanutencaocarro.application.port.embedding_generator import (
    EmbeddingGenerator,
)
from slm_assistentemanutencaocarro.application.port.knowledge_reader import (
    KnowledgeReader,
)
from slm_assistentemanutencaocarro.application.port.vector_index import (
    VectorIndex,
)


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
            vehicle_id=self.vehicle_context.get_selected(),
            top_k=top_k,
        )
