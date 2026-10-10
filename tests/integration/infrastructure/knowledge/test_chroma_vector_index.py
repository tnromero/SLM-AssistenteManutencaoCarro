import chromadb
import pytest

from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.knowledge.chroma_chunk_mapper import (
    serialize_metadata,
)
from slm_assistentemanutencaocarro.infrastructure.knowledge.chroma_vector_index import (
    ChromaVectorIndex,
)


@pytest.fixture
def vector_index(tmp_path):
    client = chromadb.PersistentClient(
        path=str(tmp_path / "vector_db")
    )

    collection = client.create_collection(
        name="test-knowledge",
        embedding_function=None,
        configuration={"hnsw": {"space": "cosine"}},
    )

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
                VehicleId(value=vehicle_id)
                if vehicle_id is not None
                else None
            ),
        )
        for document_id, vehicle_id, _ in records
    ]

    collection.add(
        ids=[chunk.id for chunk in chunks],
        documents=[chunk.content for chunk in chunks],
        embeddings=[vector for _, _, vector in records],
        metadatas=[serialize_metadata(chunk) for chunk in chunks],
    )

    return ChromaVectorIndex(collection)

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
    assert results[0].chunk.vehicle_id == VehicleId(
        value="t-cross-2022"
    )

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
