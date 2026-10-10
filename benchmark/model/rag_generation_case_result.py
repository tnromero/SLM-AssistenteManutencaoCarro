from dataclasses import dataclass


@dataclass(frozen=True)
class RagGenerationCaseResult:
    case_id: str
    question: str
    answerable: bool
    expected_answer: str
    retrieved_document_ids: tuple[str, ...]
    response: str | None
    refused: bool | None
    citations_valid: bool | None
    retrieval_time: float
    generation_time: float
    error: str | None
    refusal_format_valid: bool | None
