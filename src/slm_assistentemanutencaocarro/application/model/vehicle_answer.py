from pydantic import BaseModel


class VehicleAnswer(BaseModel):
    question: str
    answer: str
