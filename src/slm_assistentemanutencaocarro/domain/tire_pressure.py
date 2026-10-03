from pydantic import BaseModel


class TirePressure(BaseModel):
    front: float
    rear: float