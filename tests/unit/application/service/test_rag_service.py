from unittest.mock import Mock

import pytest

from slm_assistentemanutencaocarro.application.exception import (
    RagGenerationError,
)
from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (  # noqa: E501
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.model.rag_context import (
    RagContext,
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
from slm_assistentemanutencaocarro.application.service.rag_service import (
    RagService,
)


@pytest.fixture
def rag_setup():
    search_service = Mock(spec=KnowledgeSearchService)
    generator = Mock(spec=RagResponseGenerator)

    service = RagService(
        knowledge_search_service=search_service,
        response_generator=generator,
        response_validator=RagResponseValidationService(),
    )

    return service, search_service, generator

def test_generates_answer_preserving_retrieved_results(rag_setup):
    service, search_service, generator = rag_setup

    result = KnowledgeSearchResult(
        chunk=KnowledgeChunk(
            id="pneus:chunk:0",
            document_id="pneus",
            title="Cuidados com os pneus",
            content="Consulte os dados do veículo.",
            source="Material de estudo",
            position=0,
        ),
        score=0.8,
    )

    search_service.search.return_value = [result]
    generator.generate.return_value = (
        "Consulte os dados do veículo [1]."
    )

    answer = service.answer("Onde consultar a pressão?", top_k=2)

    search_service.search.assert_called_once_with(
        question="Onde consultar a pressão?",
        top_k=2,
    )
    generator.generate.assert_called_once_with(
        RagContext(
            question="Onde consultar a pressão?",
            results=(result,),
        )
    )

    assert answer.response == "Consulte os dados do veículo [1]."
    assert answer.results == (result,)

def test_skips_generation_without_results(rag_setup):
    service, search_service, generator = rag_setup
    search_service.search.return_value = []

    answer = service.answer("Onde consultar a pressão?")

    assert answer.response == RagService.NO_RESULTS_MESSAGE
    assert answer.results == ()
    generator.generate.assert_not_called()

def test_propagates_generation_failure(rag_setup):
    service, search_service, generator = rag_setup
    search_service.search.return_value = [
        Mock(spec=KnowledgeSearchResult)
    ]
    generator.generate.side_effect = RagGenerationError(
        "Ollama indisponível"
    )

    with pytest.raises(RagGenerationError):
        service.answer("Onde consultar a pressão?")

@pytest.mark.parametrize(
    ("question", "top_k"),
    [
        ("   ", 3),
        ("Qual óleo?", 0),
    ],
)
def test_rejects_invalid_input(rag_setup, question, top_k):
    service, search_service, generator = rag_setup

    with pytest.raises(ValueError):
        service.answer(question, top_k=top_k)

    search_service.search.assert_not_called()
    generator.generate.assert_not_called()

@pytest.mark.parametrize(
    "response",
    [
        "Consulte os dados do veículo.",
        "Consulte o documento [2].",
    ],
)
def test_rejects_invalid_citations(rag_setup, response):
    service, search_service, generator = rag_setup

    search_service.search.return_value = [
        Mock(spec=KnowledgeSearchResult)
    ]
    generator.generate.return_value = response

    with pytest.raises(RagGenerationError):
        service.answer("Onde consultar a pressão?")

def test_accepts_insufficient_information_response(rag_setup):
    service, search_service, generator = rag_setup

    search_service.search.return_value = [
        Mock(spec=KnowledgeSearchResult)
    ]
    generator.generate.return_value = (
        RagResponseValidationService.INSUFFICIENT_INFORMATION_MESSAGE
    )

    answer = service.answer("Qual o torque das rodas?")

    assert answer.response == (
        RagResponseValidationService.INSUFFICIENT_INFORMATION_MESSAGE
    )
