import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from slm_assistentemanutencaocarro.application.exception import (
    RagGenerationError,
)
from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.model.rag_context import (
    RagContext,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_rag_response_generator import (
    OllamaRagResponseGenerator,
)


MODULE = (
    "slm_assistentemanutencaocarro.infrastructure.ollama."
    "ollama_rag_response_generator"
)


@pytest.fixture
def chat_mock():
    with patch(f"{MODULE}.ollama.chat") as mock:
        yield mock


@pytest.fixture
def rag_context():
    return RagContext(
        question="Onde consultar a pressão?",
        results=tuple(
            KnowledgeSearchResult(
                chunk=KnowledgeChunk(
                    id=f"pneus:chunk:{position}",
                    document_id="pneus",
                    title="Cuidados com os pneus",
                    content=content,
                    source="Material de estudo",
                    position=position,
                ),
                score=0.8,
            )
            for position, content in enumerate([
                "Consulte os dados do veículo.",
                "Consulte a documentação do fabricante.",
            ])
        ),
    )


def test_sends_question_and_numbered_passages(chat_mock, rag_context):
    chat_mock.return_value = SimpleNamespace(
        message=SimpleNamespace(
            content=" Consulte os dados do veículo [1]. "
        )
    )

    response = OllamaRagResponseGenerator("qwen3:1.7b").generate(
        rag_context
    )

    payload = json.loads(
        chat_mock.call_args.kwargs["messages"][1]["content"]
    )

    assert response == "Consulte os dados do veículo [1]."
    assert payload["question"] == rag_context.question
    assert [passage["citation_id"] for passage in payload["passages"]] == [
        1,
        2,
    ]
    assert [passage["content"] for passage in payload["passages"]] == [
        result.chunk.content for result in rag_context.results
    ]


def test_rejects_context_without_passages(chat_mock):
    context = RagContext(question="Qual óleo?", results=())

    with pytest.raises(ValueError):
        OllamaRagResponseGenerator("qwen3:1.7b").generate(context)

    chat_mock.assert_not_called()


@pytest.mark.parametrize("content", [None, "", "   "])
def test_rejects_empty_response(chat_mock, rag_context, content):
    chat_mock.return_value = SimpleNamespace(
        message=SimpleNamespace(content=content)
    )

    with pytest.raises(RagGenerationError):
        OllamaRagResponseGenerator("qwen3:1.7b").generate(rag_context)


def test_wraps_ollama_failure(chat_mock, rag_context):
    chat_mock.side_effect = RuntimeError("Ollama indisponível")

    with pytest.raises(RagGenerationError):
        OllamaRagResponseGenerator("qwen3:1.7b").generate(rag_context)
