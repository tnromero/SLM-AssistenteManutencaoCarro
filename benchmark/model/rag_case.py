from pydantic import BaseModel, ConfigDict, Field, model_validator


class RagCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    expected_document_ids: list[str]
    answerable: bool
    expected_answer: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_expected_documents(self) -> "RagCase":
        if self.answerable and not self.expected_document_ids:
            raise ValueError(
                "Caso respondível deve indicar documentos esperados."
            )

        if not self.answerable and self.expected_document_ids:
            raise ValueError(
                "Caso sem resposta deve ter documentos esperados vazios."
            )

        if len(set(self.expected_document_ids)) != len(
            self.expected_document_ids
        ):
            raise ValueError("Documentos esperados duplicados.")

        return self
