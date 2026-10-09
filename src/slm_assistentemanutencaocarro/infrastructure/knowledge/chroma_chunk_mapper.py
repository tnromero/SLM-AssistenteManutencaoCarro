from pydantic import BaseModel, ConfigDict

from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class StoredChunkMetadata(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    document_id: str
    title: str
    source: str
    position: int
    is_general: bool
    vehicle_id: str


def serialize_metadata(chunk: KnowledgeChunk) -> dict:
    metadata = StoredChunkMetadata(
        document_id=chunk.document_id,
        title=chunk.title,
        source=chunk.source,
        position=chunk.position,
        is_general=chunk.vehicle_id is None,
        vehicle_id=(
            chunk.vehicle_id.value
            if chunk.vehicle_id is not None
            else ""
        ),
    )

    return metadata.model_dump()


def deserialize_chunk(
    chunk_id: str,
    content: str,
    metadata: dict,
) -> KnowledgeChunk:
    stored = StoredChunkMetadata.model_validate(metadata)

    if stored.is_general:
        if stored.vehicle_id != "":
            raise ValueError(
                "Documento geral não pode ter veículo associado."
            )
        vehicle_id = None
    else:
        if not stored.vehicle_id.strip():
            raise ValueError(
                "Documento específico deve ter veículo associado."
            )
        vehicle_id = VehicleId(value=stored.vehicle_id)

    return KnowledgeChunk(
        id=chunk_id,
        document_id=stored.document_id,
        title=stored.title,
        content=content,
        source=stored.source,
        position=stored.position,
        vehicle_id=vehicle_id,
    )
