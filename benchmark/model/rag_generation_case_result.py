from dataclasses import dataclass

from benchmark.model.rag_retrieved_passage import RagRetrievedPassage


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
    retrieved_passages: tuple[RagRetrievedPassage, ...]
