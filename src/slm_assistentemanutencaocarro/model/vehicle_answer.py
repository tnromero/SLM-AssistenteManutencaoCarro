from pydantic import BaseModel


class VehicleAnswer(BaseModel):
    question: str
    answer: str
    source: str = "vehicle.json"