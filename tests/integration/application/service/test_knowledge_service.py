import json

from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.service.knowledge_service import (
    KnowledgeService,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.persistence.markdown_knowledge_reader import (
    MarkdownKnowledgeReader,
)


def test_filters_loaded_documents_when_vehicle_changes(tmp_path):
    entries = [
        ("geral", None),
        ("t-cross", "t-cross-2022"),
        ("polo", "polo-2023"),
    ]

    manifest_entries = []

    for document_id, vehicle_id in entries:
        filename = f"{document_id}.md"

        (tmp_path / filename).write_text(
            f"# {document_id}\nConteúdo de teste.",
            encoding="utf-8",
        )

        manifest_entries.append(
            {
                "id": document_id,
                "title": document_id,
                "file": filename,
                "source": "Material de teste",
                "vehicle_id": vehicle_id,
            }
        )

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps({"documents": manifest_entries}),
        encoding="utf-8",
    )

    context = VehicleContext()
    service = KnowledgeService(
        knowledge_reader=MarkdownKnowledgeReader(manifest_path),
        vehicle_context=context,
    )

    assert [doc.id for doc in service.list_documents()] == ["geral"]

    context.select(VehicleId(value="t-cross-2022"))

    assert [doc.id for doc in service.list_documents()] == [
        "geral",
        "t-cross",
    ]

    context.select(VehicleId(value="polo-2023"))

    assert [doc.id for doc in service.list_documents()] == [
        "geral",
        "polo",
    ]