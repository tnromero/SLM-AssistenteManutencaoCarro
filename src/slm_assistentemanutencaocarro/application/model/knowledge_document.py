from dataclasses import dataclass

from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


@dataclass(frozen=True)
class KnowledgeDocument:
    id: str
    title: str
    content: str
    source: str
    vehicle_id: VehicleId | None = None
