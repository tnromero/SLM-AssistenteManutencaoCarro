from pydantic import BaseModel, ConfigDict, Field, field_validator

from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class VehicleKnowledgeSearchRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    vehicle_id: VehicleId
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("A pergunta não pode ser vazia.")
        return value


class KnowledgePassage(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    chunk_id: str
    document_id: str
    title: str
    content: str
    source: str
    score: float


class VehicleKnowledgeSearchResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    vehicle_id: VehicleId
    passages: tuple[KnowledgePassage, ...]
