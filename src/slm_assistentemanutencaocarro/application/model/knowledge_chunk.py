from dataclasses import dataclass

from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


@dataclass(frozen=True)
class KnowledgeChunk:
    id: str
    document_id: str
    title: str
    content: str
    source: str
    position: int
    vehicle_id: VehicleId | None = None
