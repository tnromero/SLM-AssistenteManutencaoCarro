import json
from unittest.mock import Mock

from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.port.embedding_generator import (
    EmbeddingGenerator,
)
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (
    KnowledgeSearchService,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.knowledge.in_memory_vector_index import (
    InMemoryVectorIndex,
)
from slm_assistentemanutencaocarro.infrastructure.knowledge.word_document_chunker import (
    WordDocumentChunker,
)
from slm_assistentemanutencaocarro.infrastructure.persistence.markdown_knowledge_reader import (
    MarkdownKnowledgeReader,
)


def test_search_ranks_eligible_chunks_without_reindexing(tmp_path):
    documents = [
        ("geral", None, "Orientações gerais."),
        ("t-cross", "t-cross-2022", "Informações do T-Cross."),
        ("polo", "polo-2023", "Informações do Polo."),
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

    generator = Mock(spec=EmbeddingGenerator)
    generator.embed_documents.side_effect = (
        lambda chunks: [
            vectors[chunk.document_id]
            for chunk in chunks
        ]
    )
    generator.embed_query.return_value = [1.0, 0.0]

    context = VehicleContext()
    service = KnowledgeSearchService(
        knowledge_reader=MarkdownKnowledgeReader(manifest_path),
        chunker=WordDocumentChunker(),
        embedding_generator=generator,
        vector_index=InMemoryVectorIndex(),
        vehicle_context=context,
    )

    assert service.build_index() == 3

    # Sem seleção, apenas o documento geral é elegível.
    results = service.search("Pergunta de teste")

    assert [result.chunk.document_id for result in results] == ["geral"]

    # Polo tem o maior score global, mas não pode aparecer para T-Cross.
    context.select(VehicleId(value="t-cross-2022"))
    results = service.search("Pergunta de teste", top_k=1)

    assert results[0].chunk.document_id == "t-cross"
    assert results[0].chunk.source == "Material de teste"
    assert results[0].chunk.content == "Informações do T-Cross."

    # Trocar o veículo altera os resultados sem gerar novos embeddings.
    context.select(VehicleId(value="polo-2023"))
    results = service.search("Pergunta de teste", top_k=1)

    assert results[0].chunk.document_id == "polo"

    generator.embed_documents.assert_called_once()
    assert generator.embed_query.call_count == 3
