from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from benchmark.benchmark.rag_retrieval_benchmark import (
    RagRetrievalBenchmark,
)
from benchmark.model.rag_case import RagCase
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (
    KnowledgeSearchService,
)


def test_calculates_document_recall_without_counting_duplicate_chunks():
    search_service = Mock(spec=KnowledgeSearchService)
    search_service.search.return_value = [
        SimpleNamespace(
            chunk=SimpleNamespace(document_id="pneus")
        ),
        SimpleNamespace(
            chunk=SimpleNamespace(document_id="pneus")
        ),
    ]

    dataset = [
        RagCase(
            id="respondivel",
            question="Pergunta de teste",
            expected_document_ids=["pneus", "oleo"],
            answerable=True,
            expected_answer="Resposta de referência",
        ),
        RagCase(
            id="sem-resposta",
            question="Pergunta sem evidência",
            expected_document_ids=[],
            answerable=False,
            expected_answer="Informação insuficiente",
        ),
    ]

    result = RagRetrievalBenchmark.evaluate(
        search_service,
        dataset,
        top_k=2,
    )

    assert len(result.cases) == 1
    assert result.hit_rate == 1.0
    assert result.mean_recall == pytest.approx(0.5)
    assert result.cases[0].retrieved_document_ids == ("pneus",)
    search_service.search.assert_called_once_with(
        question="Pergunta de teste",
        top_k=2,
    )
