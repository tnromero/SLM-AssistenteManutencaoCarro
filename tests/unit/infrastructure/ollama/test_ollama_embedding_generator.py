from types import SimpleNamespace
from unittest.mock import patch

import pytest

from slm_assistentemanutencaocarro.application.exception import (
    EmbeddingGenerationError,
)
from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_embedding_generator import (
    OllamaEmbeddingGenerator,
)

MODULE = (
    "slm_assistentemanutencaocarro.infrastructure.ollama."
    "ollama_embedding_generator"
)


@pytest.fixture
def embed_mock():
    with patch(f"{MODULE}.ollama.embed") as mock:
        yield mock


def make_chunk(position: int) -> KnowledgeChunk:
    return KnowledgeChunk(
        id=f"pneus:chunk:{position}",
        document_id="pneus",
        title="Pneus",
        content=f"Trecho {position}",
        source="Material de teste",
        position=position,
    )


def test_embeds_query(embed_mock):
    embed_mock.return_value = SimpleNamespace(
        embeddings=[[0.1, 0.2]],
    )

    vector = OllamaEmbeddingGenerator().embed_query(
        "Como consultar a calibragem?"
    )

    assert vector == [0.1, 0.2]
    embed_mock.assert_called_once_with(
        model="embeddinggemma:300m",
        input=[
            "task: search result | query: Como consultar a calibragem?"
        ],
        truncate=False,
    )


def test_embeds_documents_in_order(embed_mock):
    embed_mock.return_value = SimpleNamespace(
        embeddings=[[0.1, 0.2], [0.3, 0.4]],
    )

    vectors = OllamaEmbeddingGenerator().embed_documents(
        [make_chunk(0), make_chunk(1)]
    )

    assert vectors == [[0.1, 0.2], [0.3, 0.4]]
    assert embed_mock.call_args.kwargs["input"] == [
        "title: Pneus | text: Trecho 0",
        "title: Pneus | text: Trecho 1",
    ]


def test_empty_batch_skips_ollama(embed_mock):
    assert OllamaEmbeddingGenerator().embed_documents([]) == []
    embed_mock.assert_not_called()


@pytest.mark.parametrize(
    "vectors",
    [
        [],
        [[]],
        [[0.0, 0.0]],
        [[float("nan"), 0.1]],
        [[0.1], [0.2]],
    ],
)
def test_rejects_invalid_response(embed_mock, vectors):
    embed_mock.return_value = SimpleNamespace(embeddings=vectors)

    with pytest.raises(EmbeddingGenerationError):
        OllamaEmbeddingGenerator().embed_query("Qual óleo?")


def test_wraps_ollama_failure(embed_mock):
    embed_mock.side_effect = RuntimeError("Ollama indisponível")

    with pytest.raises(EmbeddingGenerationError):
        OllamaEmbeddingGenerator().embed_query("Qual óleo?")
