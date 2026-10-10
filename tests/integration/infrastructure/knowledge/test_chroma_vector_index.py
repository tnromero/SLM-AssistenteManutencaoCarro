from unittest.mock import Mock, patch

import chromadb
import pytest

from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.exception import VectorIndexError
from slm_assistentemanutencaocarro.application.model.embedded_chunk import (
    EmbeddedChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
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
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (  # noqa: E501
    KnowledgeSearchService,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.knowledge.chroma_vector_index import (  # noqa: E501
    ChromaVectorIndex,
)


@pytest.fixture
def vector_index(tmp_path):
    client = chromadb.PersistentClient(path=str(tmp_path / "vector_db"))

    records = [
        ("geral", None, [0.0, 1.0]),
        ("t-cross", "t-cross-2022", [0.8, 0.2]),
        ("polo", "polo-2023", [1.0, 0.0]),
    ]

    chunks = [
        KnowledgeChunk(
            id=f"{document_id}:chunk:0",
            document_id=document_id,
            title=document_id,
            content=f"Conteúdo de {document_id}.",
            source="Material de teste",
            position=0,
            vehicle_id=(
                VehicleId(value=vehicle_id) if vehicle_id is not None else None
            ),
        )
        for document_id, vehicle_id, _ in records
    ]

    index = ChromaVectorIndex(
        client=client,
        collection_name="test-knowledge",
        embedding_model="test-model",
    )

    index.replace([
        EmbeddedChunk(
            chunk=chunk,
            vector=tuple(vector),
        )
        for chunk, (_, _, vector) in zip(
            chunks,
            records,
            strict=True,
        )
    ])

    return index


def test_without_vehicle_returns_only_general_chunks(vector_index):
    results = vector_index.search(
        query_vector=[1.0, 0.0],
        vehicle_id=None,
    )

    assert [result.chunk.document_id for result in results] == ["geral"]
    assert results[0].score == pytest.approx(0.0, abs=1e-6)


def test_filters_vehicle_before_selecting_top_k(vector_index):
    results = vector_index.search(
        query_vector=[1.0, 0.0],
        vehicle_id=VehicleId(value="t-cross-2022"),
        top_k=1,
    )

    # Polo tem o maior score global, mas não é elegível.
    assert results[0].chunk.document_id == "t-cross"
    assert results[0].chunk.vehicle_id == VehicleId(value="t-cross-2022")


def test_returns_ranked_results_with_similarity_scores(vector_index):
    results = vector_index.search(
        query_vector=[1.0, 0.0],
        vehicle_id=VehicleId(value="polo-2023"),
        top_k=3,
    )

    assert [result.chunk.document_id for result in results] == [
        "polo",
        "geral",
    ]
    assert [result.score for result in results] == pytest.approx(
        [1.0, 0.0],
        abs=1e-6,
    )
    assert results[0].chunk.source == "Material de teste"


@pytest.mark.parametrize(
    "query_vector",
    [
        [],
        [0.0, 0.0],
        [float("nan"), 1.0],
    ],
)
def test_rejects_invalid_query_vector(vector_index, query_vector):
    with pytest.raises(ValueError):
        vector_index.search(
            query_vector=query_vector,
            vehicle_id=None,
        )

def make_entry(chunk_id: str) -> EmbeddedChunk:
    return EmbeddedChunk(
        chunk=KnowledgeChunk(
            id=chunk_id,
            document_id=chunk_id,
            title=chunk_id,
            content="Conteúdo de teste.",
            source="Teste",
            position=0,
        ),
        vector=(1.0, 0.0),
    )
def test_replaces_active_index(vector_index):
    vector_index.replace([make_entry("novo")])

    results = vector_index.search([1.0, 0.0], vehicle_id=None)

    assert [result.chunk.id for result in results] == ["novo"]

def test_write_failure_preserves_previous_index(vector_index):
    previous = vector_index.search([1.0, 0.0], vehicle_id=None)

    with patch.object(
        chromadb.Collection,
        "add",
        side_effect=RuntimeError("Falha na gravação"),
    ):
        with pytest.raises(VectorIndexError):
            vector_index.replace([make_entry("novo")])

    assert (
        vector_index.search([1.0, 0.0], vehicle_id=None)
        == previous
    )

def test_reopens_active_index(tmp_path):
    path = str(tmp_path / "vector_db")

    first = ChromaVectorIndex(
        client=chromadb.PersistentClient(path=path),
        collection_name="test-knowledge",
        embedding_model="test-model",
    )
    first.replace([make_entry("persistido")])

    restored = ChromaVectorIndex(
        client=chromadb.PersistentClient(path=path),
        collection_name="test-knowledge",
        embedding_model="test-model",
    )

    results = restored.search([1.0, 0.0], vehicle_id=None)

    assert results[0].chunk.id == "persistido"
    assert restored.is_ready() is True
    assert restored.count() == 1

def test_empty_replacement_creates_ready_index(tmp_path):
    index = ChromaVectorIndex(
        client=chromadb.PersistentClient(
            path=str(tmp_path / "vector_db")
        ),
        collection_name="test-knowledge",
        embedding_model="test-model",
    )

    assert index.is_ready() is False
    assert index.count() == 0

    index.replace([])

    assert index.is_ready() is True
    assert index.count() == 0
    assert index.search([1.0, 0.0], vehicle_id=None) == []

def test_service_searches_persisted_index_without_rebuilding(tmp_path):
    path = str(tmp_path / "vector_db")

    first_index = ChromaVectorIndex(
        client=chromadb.PersistentClient(path=path),
        collection_name="test-knowledge",
        embedding_model="test-model",
    )
    first_index.replace([make_entry("persistido")])

    restored_index = ChromaVectorIndex(
        client=chromadb.PersistentClient(path=path),
        collection_name="test-knowledge",
        embedding_model="test-model",
    )

    reader = Mock(spec=KnowledgeReader)
    chunker = Mock(spec=DocumentChunker)
    generator = Mock(spec=EmbeddingGenerator)
    generator.embed_query.return_value = [1.0, 0.0]

    service = KnowledgeSearchService(
        knowledge_reader=reader,
        chunker=chunker,
        embedding_generator=generator,
        vector_index=restored_index,
        vehicle_context=VehicleContext(),
    )

    results = service.search("Pergunta de teste")

    assert results[0].chunk.id == "persistido"

    reader.list_documents.assert_not_called()
    chunker.split.assert_not_called()
    generator.embed_documents.assert_not_called()
    generator.embed_query.assert_called_once_with("Pergunta de teste")
