from pydantic import BaseModel, ConfigDict

from slm_assistentemanutencaocarro.application.model.vehicle.vehicle_summary import (
    VehicleSummary,
)


class ListVehiclesRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class ListVehiclesResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    vehicles: tuple[VehicleSummary, ...]
