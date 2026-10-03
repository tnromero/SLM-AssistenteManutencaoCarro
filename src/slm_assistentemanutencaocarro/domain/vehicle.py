from pydantic import BaseModel

from slm_assistentemanutencaocarro.domain.tire_pressure import TirePressure
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class Vehicle(BaseModel):
    id: VehicleId
    brand: str
    model: str
    year: int
    engine: str

    engine_oil: str | None = None
    tire_pressure: TirePressure | None = None
    tire_size: str | None = None