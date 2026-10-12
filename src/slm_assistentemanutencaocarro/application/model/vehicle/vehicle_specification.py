import enum

from pydantic import BaseModel, ConfigDict

from slm_assistentemanutencaocarro.domain.tire_pressure import TirePressure
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class VehicleSpecification(enum.StrEnum):
    ENGINE_OIL = "engine_oil"
    TIRE_PRESSURE = "tire_pressure"
    TIRE_SIZE = "tire_size"


class VehicleSpecificationRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    vehicle_id: VehicleId
    specification: VehicleSpecification


class VehicleSpecificationResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    vehicle_id: VehicleId
    specification: VehicleSpecification
    value: str | TirePressure | None
