from pydantic import BaseModel


class Vehicle(BaseModel):
    brand: str
    model: str
    year: int
    engine: str
    engine_oil: str
    tire_size: str
    tire_pressure_front: float
    tire_pressure_rear: float