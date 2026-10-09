import pytest

from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.knowledge.chroma_chunk_mapper import (
    deserialize_chunk,
    serialize_metadata,
)


@pytest.mark.parametrize(
    "vehicle_id",
    [
        None,
        VehicleId(value="t-cross-2022"),
    ],
)
def test_preserves_chunk_fields(vehicle_id):
    chunk = KnowledgeChunk(
        id="pneus:chunk:0",
        document_id="pneus",
        title="Cuidados com os pneus",
        content="Consulte os dados do veículo.",
        source="Material de teste",
        position=0,
        vehicle_id=vehicle_id,
    )

    restored = deserialize_chunk(
        chunk_id=chunk.id,
        content=chunk.content,
        metadata=serialize_metadata(chunk),
    )

    assert restored == chunk

@pytest.mark.parametrize(
    ("is_general", "vehicle_id"),
    [
        (True, "t-cross-2022"),
        (False, ""),
    ],
)
def test_rejects_inconsistent_vehicle_metadata(is_general, vehicle_id):
    metadata = {
        "document_id": "pneus",
        "title": "Pneus",
        "source": "Teste",
        "position": 0,
        "is_general": is_general,
        "vehicle_id": vehicle_id,
    }

    with pytest.raises(ValueError):
        deserialize_chunk(
            chunk_id="pneus:chunk:0",
            content="Conteúdo.",
            metadata=metadata,
        )
