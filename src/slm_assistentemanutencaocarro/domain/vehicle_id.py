from pydantic import BaseModel


class VehicleId(BaseModel):
    value: str