from unittest.mock import Mock

import pytest

from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.model.knowledge_document import (
    KnowledgeDocument,
)
from slm_assistentemanutencaocarro.application.port.knowledge_reader import (
    KnowledgeReader,
)
from slm_assistentemanutencaocarro.application.service.knowledge_service import (
    KnowledgeService,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


@pytest.fixture
def knowledge_setup():
    documents = [
        KnowledgeDocument(
            id="geral",
            title="Orientações gerais",
            content="Conteúdo geral.",
            source="Material de estudo",
        ),
        KnowledgeDocument(
            id="t-cross",
            title="Documento do T-Cross",
            content="Conteúdo de teste do T-Cross.",
            source="Material de estudo",
            vehicle_id=VehicleId(value="t-cross-2022"),
        ),
        KnowledgeDocument(
            id="polo",
            title="Documento do Polo",
            content="Conteúdo de teste do Polo.",
            source="Material de estudo",
            vehicle_id=VehicleId(value="polo-2023"),
        ),
    ]

    reader = Mock(spec=KnowledgeReader)
    reader.list_documents.return_value = documents

    context = VehicleContext()
    service = KnowledgeService(
        knowledge_reader=reader,
        vehicle_context=context,
    )

    return service, context


def test_returns_only_general_documents_without_selected_vehicle(
    knowledge_setup,
):
    service, _ = knowledge_setup

    assert [doc.id for doc in service.list_documents()] == ["geral"]


@pytest.mark.parametrize(
    ("vehicle_id", "expected_ids"),
    [
        ("t-cross-2022", ["geral", "t-cross"]),
        ("polo-2023", ["geral", "polo"]),
    ],
)
def test_returns_general_and_selected_vehicle_documents(
    knowledge_setup,
    vehicle_id,
    expected_ids,
):
    service, context = knowledge_setup
    context.select(VehicleId(value=vehicle_id))

    assert [doc.id for doc in service.list_documents()] == expected_ids


def test_vehicle_change_updates_available_documents(knowledge_setup):
    service, context = knowledge_setup

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
