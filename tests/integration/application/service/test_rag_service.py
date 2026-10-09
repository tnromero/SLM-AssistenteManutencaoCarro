import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.exception import (
    RagGenerationError,
)
from slm_assistentemanutencaocarro.application.port.embedding_generator import (
    EmbeddingGenerator,
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
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.knowledge.in_memory_vector_index import (  # noqa: E501
    InMemoryVectorIndex,
)
from slm_assistentemanutencaocarro.infrastructure.knowledge.word_document_chunker import (  # noqa: E501
    WordDocumentChunker,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_rag_response_generator import (  # noqa: E501
    OllamaRagResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.persistence.markdown_knowledge_reader import (  # noqa: E501
    MarkdownKnowledgeReader,
)


@pytest.fixture
def rag_flow(tmp_path):
    documents = [
        ("geral", None, "Consulte a documentação do fabricante."),
        (
            "t-cross",
            "t-cross-2022",
            "Consulte os dados cadastrados do T-Cross.",
        ),
        (
            "polo",
            "polo-2023",
            "Consulte os dados cadastrados do Polo.",
        ),
    ]

    entries = []

    for document_id, vehicle_id, content in documents:
        filename = f"{document_id}.md"
        (tmp_path / filename).write_text(content, encoding="utf-8")

        entries.append({
            "id": document_id,
            "title": document_id,
            "file": filename,
            "source": "Material de teste",
            "vehicle_id": vehicle_id,
        })

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps({"documents": entries}),
        encoding="utf-8",
    )

    vectors = {
        "geral": [0.0, 1.0],
        "t-cross": [0.8, 0.2],
        "polo": [1.0, 0.0],
    }

    embedding_generator = Mock(spec=EmbeddingGenerator)
    embedding_generator.embed_documents.side_effect = (
        lambda chunks: [
            vectors[chunk.document_id] for chunk in chunks
        ]
    )
    embedding_generator.embed_query.return_value = [1.0, 0.0]

    vehicle_context = VehicleContext()
    vehicle_context.select(VehicleId(value="t-cross-2022"))

    search_service = KnowledgeSearchService(
        knowledge_reader=MarkdownKnowledgeReader(manifest_path),
        chunker=WordDocumentChunker(),
        embedding_generator=embedding_generator,
        vector_index=InMemoryVectorIndex(),
        vehicle_context=vehicle_context,
    )
    search_service.build_index()

    rag_service = RagService(
        knowledge_search_service=search_service,
        response_generator=OllamaRagResponseGenerator("qwen3:1.7b"),
        response_validator=RagResponseValidationService(),
    )

    module = (
        "slm_assistentemanutencaocarro.infrastructure.ollama."
        "ollama_rag_response_generator"
    )

    with patch(f"{module}.ollama.chat") as chat:
        yield rag_service, vehicle_context, chat

def test_generates_answer_using_selected_vehicle_document(rag_flow):
    service, _, chat = rag_flow

    chat.return_value = SimpleNamespace(
        message=SimpleNamespace(
            content="Consulte os dados cadastrados do T-Cross [1]."
        )
    )

    answer = service.answer("Onde consultar os dados?", top_k=1)

    payload = json.loads(
        chat.call_args.kwargs["messages"][1]["content"]
    )

    assert payload["question"] == "Onde consultar os dados?"
    assert payload["passages"] == [
        {
            "citation_id": 1,
            "title": "t-cross",
            "content": "Consulte os dados cadastrados do T-Cross.",
        }
    ]

    assert answer.response == (
        "Consulte os dados cadastrados do T-Cross [1]."
    )
    assert answer.results[0].chunk.document_id == "t-cross"
    assert answer.results[0].chunk.source == "Material de teste"

def test_vehicle_change_updates_rag_context(rag_flow):
    service, vehicle_context, chat = rag_flow

    vehicle_context.select(VehicleId(value="polo-2023"))

    chat.return_value = SimpleNamespace(
        message=SimpleNamespace(
            content="Consulte os dados cadastrados do Polo [1]."
        )
    )

    answer = service.answer("Onde consultar os dados?", top_k=1)

    payload = json.loads(
        chat.call_args.kwargs["messages"][1]["content"]
    )

    assert payload["passages"][0]["title"] == "polo"
    assert answer.results[0].chunk.document_id == "polo"

@pytest.mark.parametrize(
    "response",
    [
        "Consulte os dados cadastrados.",
        "Consulte o documento [9].",
    ],
)
def test_rejects_generated_answer_with_invalid_citations(
    rag_flow,
    response,
):
    service, _, chat = rag_flow
    chat.return_value = SimpleNamespace(
        message=SimpleNamespace(content=response)
    )

    with pytest.raises(RagGenerationError):
        service.answer("Onde consultar os dados?", top_k=1)
