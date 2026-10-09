import pytest

from slm_assistentemanutencaocarro.application.model.knowledge_document import (
    KnowledgeDocument,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.knowledge.word_document_chunker import (
    WordDocumentChunker,
)


def make_document(content: str) -> KnowledgeDocument:
    return KnowledgeDocument(
        id="pneus",
        title="Cuidados com os pneus",
        content=content,
        source="Material de teste",
        vehicle_id=VehicleId(value="t-cross-2022"),
    )


def test_splits_with_overlap_preserving_metadata():
    document = make_document("um dois três quatro cinco seis sete")

    chunks = WordDocumentChunker(
        chunk_size=4,
        overlap=1,
    ).split(document)

    assert [chunk.content for chunk in chunks] == [
        "um dois três quatro",
        "quatro cinco seis sete",
    ]
    assert [chunk.id for chunk in chunks] == [
        "pneus:chunk:0",
        "pneus:chunk:1",
    ]
    assert [chunk.position for chunk in chunks] == [0, 1]

    for chunk in chunks:
        assert chunk.document_id == document.id
        assert chunk.title == document.title
        assert chunk.source == document.source
        assert chunk.vehicle_id == document.vehicle_id


def test_preserves_short_final_chunk():
    document = make_document("um dois três quatro cinco")

    chunks = WordDocumentChunker(
        chunk_size=3,
        overlap=0,
    ).split(document)

    assert [chunk.content for chunk in chunks] == [
        "um dois três",
        "quatro cinco",
    ]


def test_short_document_produces_one_chunk():
    chunks = WordDocumentChunker().split(
        make_document("Documento curto.")
    )

    assert len(chunks) == 1
    assert chunks[0].content == "Documento curto."


def test_empty_document_produces_no_chunks():
    assert WordDocumentChunker().split(make_document("   ")) == []


@pytest.mark.parametrize(
    ("chunk_size", "overlap"),
    [
        (0, 0),
        (4, -1),
        (4, 4),
        (4, 5),
    ],
)
def test_rejects_invalid_configuration(chunk_size, overlap):
    with pytest.raises(ValueError):
        WordDocumentChunker(
            chunk_size=chunk_size,
            overlap=overlap,
        )
