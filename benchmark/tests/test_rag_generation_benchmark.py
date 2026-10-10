from unittest.mock import Mock

import pytest

from benchmark.benchmark.rag_generation_benchmark import RagGenerationBenchmark
from benchmark.model.rag_case import RagCase
from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (  # noqa: E501
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.port.rag_response_generator import (  # noqa: E501
    RagResponseGenerator,
)
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (  # noqa: E501
    KnowledgeSearchService,
)
from slm_assistentemanutencaocarro.application.service.rag_response_validation_service import (  # noqa: E501
    RagResponseValidationService,
)


@pytest.mark.parametrize(
    ("answerable", "response", "expected_refusal", "expected_valid"),
    [
        (
            True,
            "Consulte a documentação [1].",
            False,
            True,
        ),
        (
            True,
            RagResponseValidationService.INSUFFICIENT_INFORMATION_MESSAGE,
            True,
            True,
        ),
        (
            False,
            RagResponseValidationService.INSUFFICIENT_INFORMATION_MESSAGE,
            True,
            True,
        ),
        (
            True,
            "Consulte a documentação [9].",
            False,
            False,
        ),
    ],
)
def test_records_refusals_and_citation_validation(
    answerable,
    response,
    expected_refusal,
    expected_valid,
):
    search = Mock(spec=KnowledgeSearchService)
    generator = Mock(spec=RagResponseGenerator)

    chunk = Mock(spec=KnowledgeChunk)
    chunk.document_id = "pneus"

    search.search.return_value = [
        KnowledgeSearchResult(chunk=chunk, score=0.8)
    ]
    generator.generate.return_value = response

    case = RagCase(
        id="teste",
        question="Pergunta",
        expected_document_ids=["pneus"] if answerable else [],
        answerable=answerable,
        expected_answer="Referência",
    )

    result = RagGenerationBenchmark.evaluate(
        search_service=search,
        generator=generator,
        validator=RagResponseValidationService(),
        dataset=[case],
    )[0]

    assert result.response == response
    assert result.refused is expected_refusal
    assert result.citations_valid is expected_valid
    assert result.error is None
