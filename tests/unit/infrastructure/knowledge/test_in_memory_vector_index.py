import pytest

from slm_assistentemanutencaocarro.application.model.embedded_chunk import (
    EmbeddedChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.knowledge.in_memory_vector_index import (
    InMemoryVectorIndex,
)


def make_entry(
    chunk_id: str,
    vector: tuple[float, ...],
    vehicle_id: str | None = None,
) -> EmbeddedChunk:
    return EmbeddedChunk(
        chunk=KnowledgeChunk(
            id=chunk_id,
            document_id=chunk_id,
            title=chunk_id,
            content="Conteúdo de teste.",
            source="Teste",
            position=0,
            vehicle_id=(
                VehicleId(value=vehicle_id)
                if vehicle_id is not None
                else None
            ),
        ),
        vector=vector,
    )


def test_ranks_by_cosine_similarity():
    index = InMemoryVectorIndex()
    index.replace([
        make_entry("oposto", (-1.0, 0.0)),
        make_entry("perpendicular", (0.0, 1.0)),
        make_entry("proximo", (2.0, 0.0)),
    ])

    results = index.search([1.0, 0.0], vehicle_id=None)

    assert [result.chunk.id for result in results] == [
        "proximo",
        "perpendicular",
        "oposto",
    ]
    assert [result.score for result in results] == pytest.approx([
        1.0,
        0.0,
        -1.0,
    ])


def test_filters_vehicle_before_selecting_top_k():
    index = InMemoryVectorIndex()
    index.replace([
        make_entry("polo", (1.0, 0.0), "polo-2023"),
        make_entry("t-cross", (0.8, 0.2), "t-cross-2022"),
        make_entry("geral", (0.0, 1.0)),
    ])

    results = index.search(
        [1.0, 0.0],
        vehicle_id=VehicleId(value="t-cross-2022"),
        top_k=1,
    )

    assert [result.chunk.id for result in results] == ["t-cross"]


def test_without_vehicle_returns_only_general_chunks():
    index = InMemoryVectorIndex()
    index.replace([
        make_entry("especifico", (1.0, 0.0), "t-cross-2022"),
        make_entry("geral", (0.0, 1.0)),
    ])

    results = index.search([1.0, 0.0], vehicle_id=None)

    assert [result.chunk.id for result in results] == ["geral"]


def test_invalid_replacement_preserves_previous_index():
    index = InMemoryVectorIndex()
    index.replace([make_entry("anterior", (1.0, 0.0))])

    with pytest.raises(ValueError):
        index.replace([
            make_entry("novo", (1.0, 0.0)),
            make_entry("invalido", (1.0,)),
        ])

    results = index.search([1.0, 0.0], vehicle_id=None)

    assert results[0].chunk.id == "anterior"


def test_rejects_incompatible_query_dimension():
    index = InMemoryVectorIndex()
    index.replace([make_entry("documento", (1.0, 0.0))])

    with pytest.raises(ValueError):
        index.search([1.0], vehicle_id=None)


def test_empty_index_returns_no_results():
    assert InMemoryVectorIndex().search(
        [1.0, 0.0],
        vehicle_id=None,
    ) == []
