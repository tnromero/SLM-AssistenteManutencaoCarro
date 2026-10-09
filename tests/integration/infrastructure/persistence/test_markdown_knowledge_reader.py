import json

import pytest

from slm_assistentemanutencaocarro.application.exception import (
    KnowledgeReadError,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.persistence.markdown_knowledge_reader import (
    MarkdownKnowledgeReader,
)


@pytest.fixture
def knowledge_files(tmp_path):
    document_path = tmp_path / "pneus.md"
    document_path.write_text(
        "# Pneus\nConsulte os dados do veículo.",
        encoding="utf-8",
    )

    manifest_path = tmp_path / "manifest.json"

    def write_manifest(entries):
        manifest_path.write_text(
            json.dumps({"documents": entries}),
            encoding="utf-8",
        )
        return MarkdownKnowledgeReader(manifest_path)

    entry = {
        "id": "documento-pneus",
        "title": "Pneus",
        "file": "pneus.md",
        "source": "Material de estudo",
        "vehicle_id": None,
    }

    return write_manifest, entry, document_path


def test_loads_general_document(knowledge_files):
    write_manifest, entry, _ = knowledge_files

    documents = write_manifest([entry]).list_documents()

    assert len(documents) == 1
    assert documents[0].id == "documento-pneus"
    assert documents[0].title == "Pneus"
    assert documents[0].source == "Material de estudo"
    assert documents[0].vehicle_id is None
    assert "Consulte os dados do veículo." in documents[0].content


def test_loads_vehicle_specific_document(knowledge_files):
    write_manifest, entry, _ = knowledge_files
    entry["vehicle_id"] = "t-cross-2022"

    document = write_manifest([entry]).list_documents()[0]

    assert document.vehicle_id == VehicleId(value="t-cross-2022")


def test_rejects_duplicate_ids(knowledge_files):
    write_manifest, entry, _ = knowledge_files

    with pytest.raises(KnowledgeReadError):
        write_manifest([entry, entry]).list_documents()


def test_rejects_empty_document(knowledge_files):
    write_manifest, entry, document_path = knowledge_files
    document_path.write_text("   ", encoding="utf-8")

    with pytest.raises(KnowledgeReadError):
        write_manifest([entry]).list_documents()


def test_rejects_missing_document(knowledge_files):
    write_manifest, entry, _ = knowledge_files
    entry["file"] = "inexistente.md"

    with pytest.raises(KnowledgeReadError):
        write_manifest([entry]).list_documents()


def test_rejects_invalid_manifest(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text("JSON inválido", encoding="utf-8")

    with pytest.raises(KnowledgeReadError):
        MarkdownKnowledgeReader(manifest_path).list_documents()
