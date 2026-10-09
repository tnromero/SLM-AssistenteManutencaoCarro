from unittest.mock import Mock

import pytest

from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.model.rag_context import (
    RagContext,
)
from slm_assistentemanutencaocarro.application.service.rag_response_validation_service import (
    RagResponseValidationService,
)


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        ("Consulte os dados do veículo [1].", True),
        ("Consulte as fontes [1] e [2].", True),
        ("Consulte o documento [3].", False),
        ("Consulte o documento [0].", False),
        ("Consulte o documento [-1].", False),
        ("Consulte os dados do veículo.", False),
        ("", False),
        (
            RagResponseValidationService.INSUFFICIENT_INFORMATION_MESSAGE,
            True,
        ),
    ],
)
def test_validates_citation_identifiers(response, expected):
    context = RagContext(
        question="Onde consultar a pressão?",
        results=(
            Mock(spec=KnowledgeSearchResult),
            Mock(spec=KnowledgeSearchResult),
        ),
    )

    assert RagResponseValidationService().validate(
        context=context,
        response=response,
    ) is expected
