from pydantic import BaseModel, ConfigDict


class VehicleSummary(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    brand: str
    model: str
    year: int
    engine: str
