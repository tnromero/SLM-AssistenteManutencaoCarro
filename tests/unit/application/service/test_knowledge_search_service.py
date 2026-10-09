from unittest.mock import Mock

import pytest

from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.exception import EmbeddingGenerationError, KnowledgeIndexNotReadyError
from slm_assistentemanutencaocarro.application.model.embedded_chunk import EmbeddedChunk
from slm_assistentemanutencaocarro.application.model.knowledge_chunk import KnowledgeChunk
from slm_assistentemanutencaocarro.application.model.knowledge_document import KnowledgeDocument
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
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (
    KnowledgeSearchService,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


@pytest.fixture
def search_setup():
    reader = Mock(spec=KnowledgeReader)
    chunker = Mock(spec=DocumentChunker)
    generator = Mock(spec=EmbeddingGenerator)
    index = Mock(spec=VectorIndex)
    context = VehicleContext()

    service = KnowledgeSearchService(
        knowledge_reader=reader,
        chunker=chunker,
        embedding_generator=generator,
        vector_index=index,
        vehicle_context=context,
    )

    return service, reader, chunker, generator, index, context

def test_builds_index_preserving_chunk_vector_association(search_setup):
    service, reader, chunker, generator, index, _ = search_setup

    document = KnowledgeDocument(
        id="pneus",
        title="Pneus",
        content="Conteúdo.",
        source="Teste",
    )
    chunk = KnowledgeChunk(
        id="pneus:chunk:0",
        document_id="pneus",
        title="Pneus",
        content="Conteúdo.",
        source="Teste",
        position=0,
    )

    reader.list_documents.return_value = [document]
    chunker.split.return_value = [chunk]
    generator.embed_documents.return_value = [[0.1, 0.2]]

    assert service.build_index() == 1

    chunker.split.assert_called_once_with(document)
    generator.embed_documents.assert_called_once_with([chunk])
    index.replace.assert_called_once_with([
        EmbeddedChunk(chunk=chunk, vector=(0.1, 0.2)),
    ])

def test_search_uses_current_vehicle_without_rebuilding(search_setup):
    service, reader, chunker, generator, index, context = search_setup

    reader.list_documents.return_value = [Mock(spec=KnowledgeDocument)]
    chunker.split.return_value = [Mock(spec=KnowledgeChunk)]
    generator.embed_documents.return_value = [[1.0, 0.0]]
    generator.embed_query.return_value = [0.8, 0.2]
    index.search.return_value = []

    service.build_index()

    for vehicle_value in ["t-cross-2022", "polo-2023"]:
        vehicle_id = VehicleId(value=vehicle_value)
        context.select(vehicle_id)

        assert service.search("Como consultar a pressão?", top_k=2) == []

        index.search.assert_called_with(
            query_vector=[0.8, 0.2],
            vehicle_id=vehicle_id,
            top_k=2,
        )

    generator.embed_documents.assert_called_once()
    index.replace.assert_called_once()

def test_search_requires_built_index(search_setup):
    service, _, _, generator, _, _ = search_setup

    with pytest.raises(KnowledgeIndexNotReadyError):
        service.search("Qual óleo?")

    generator.embed_query.assert_not_called()

def test_empty_collection_skips_embeddings(search_setup):
    service, reader, _, generator, index, _ = search_setup
    reader.list_documents.return_value = []

    assert service.build_index() == 0
    assert service.search("Qual óleo?") == []

    index.replace.assert_called_once_with([])
    generator.embed_documents.assert_not_called()
    generator.embed_query.assert_not_called()

def test_embedding_failure_does_not_replace_index(search_setup):
    service, reader, chunker, generator, index, _ = search_setup

    reader.list_documents.return_value = [Mock(spec=KnowledgeDocument)]
    chunker.split.return_value = [Mock(spec=KnowledgeChunk)]
    generator.embed_documents.side_effect = EmbeddingGenerationError(
        "Falha ao gerar embeddings"
    )

    with pytest.raises(EmbeddingGenerationError):
        service.build_index()

    index.replace.assert_not_called()