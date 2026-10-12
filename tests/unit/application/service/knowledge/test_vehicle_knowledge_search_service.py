from unittest.mock import Mock

import pytest

from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.model.knowledge.knowledge_chunk import (  # noqa: E501
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge.knowledge_search_result import (  # noqa: E501
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.model.knowledge.vehicle_knowledge_search import (  # noqa: E501
    VehicleKnowledgeSearchRequest,
)
from slm_assistentemanutencaocarro.application.port.vehicle.vehicle_reader import (  # noqa: E501
    VehicleReader,
)
from slm_assistentemanutencaocarro.application.service.knowledge.knowledge_search_service import (  # noqa: E501
    KnowledgeSearchService,
)
from slm_assistentemanutencaocarro.application.service.knowledge.vehicle_knowledge_search_service import (  # noqa: E501
    VehicleKnowledgeSearchService,
)
from slm_assistentemanutencaocarro.domain.exception import VehicleNotFoundError
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


@pytest.fixture
def dependencies():
    reader = Mock(spec=VehicleReader)
    search = Mock(spec=KnowledgeSearchService)
    service = VehicleKnowledgeSearchService(
        vehicle_reader=reader,
        search_service=search,
    )
    return reader, search, service


def test_forwards_request_and_preserves_passage_evidence(dependencies):
    reader, search, service = dependencies
    vehicle_id = VehicleId(value="vehicle-test")

    search.search.return_value = [
        KnowledgeSearchResult(
            chunk=KnowledgeChunk(
                id="pneus:chunk:0",
                document_id="pneus",
                title="Cuidados com os pneus",
                content="Consulte a documentação do fabricante.",
                source="Documento de teste",
                position=0,
                vehicle_id=vehicle_id,
            ),
            score=0.85,
        )
    ]

    result = service.execute(
        VehicleKnowledgeSearchRequest(
            vehicle_id=vehicle_id,
            question="Onde consultar a pressão?",
            top_k=2,
        )
    )

    reader.get_vehicle.assert_called_once_with(vehicle_id)
    search.search.assert_called_once_with(
        question="Onde consultar a pressão?",
        top_k=2,
        vehicle_id=vehicle_id,
    )
    assert result.model_dump(mode="json") == {
        "vehicle_id": {"value": "vehicle-test"},
        "passages": [
            {
                "chunk_id": "pneus:chunk:0",
                "document_id": "pneus",
                "title": "Cuidados com os pneus",
                "content": "Consulte a documentação do fabricante.",
                "source": "Documento de teste",
                "score": 0.85,
            }
        ],
    }


def test_returns_empty_passages_when_search_has_no_results(dependencies):
    _, search, service = dependencies
    search.search.return_value = []
    vehicle_id = VehicleId(value="vehicle-test")

    result = service.execute(
        VehicleKnowledgeSearchRequest(
            vehicle_id=vehicle_id,
            question="Onde consultar a pressão?",
        )
    )

    assert result.vehicle_id == vehicle_id
    assert result.passages == ()


def test_unknown_vehicle_prevents_search(dependencies):
    reader, search, service = dependencies
    reader.get_vehicle.side_effect = VehicleNotFoundError("Não encontrado")

    request = VehicleKnowledgeSearchRequest(
        vehicle_id=VehicleId(value="missing"),
        question="Onde consultar a pressão?",
    )

    with pytest.raises(VehicleNotFoundError):
        service.execute(request)

    search.search.assert_not_called()

@pytest.mark.parametrize("explicit_vehicle", [False, True])
def test_search_vehicle_filter_preserves_session(explicit_vehicle):
    selected_id = VehicleId(value="selected-vehicle")
    requested_id = VehicleId(value="requested-vehicle")

    context = VehicleContext()
    context.select(selected_id)

    embedding_generator = Mock()
    embedding_generator.embed_query.return_value = [0.1, 0.2]

    vector_index = Mock()
    vector_index.is_ready.return_value = True
    vector_index.count.return_value = 2
    vector_index.search.return_value = []

    service = KnowledgeSearchService(
        knowledge_reader=Mock(),
        chunker=Mock(),
        embedding_generator=embedding_generator,
        vector_index=vector_index,
        vehicle_context=context,
    )

    if explicit_vehicle:
        result = service.search(
            question="Onde consultar a pressão?",
            top_k=2,
            vehicle_id=requested_id,
        )
    else:
        result = service.search(
            question="Onde consultar a pressão?",
            top_k=2,
        )

    vector_index.search.assert_called_once_with(
        query_vector=[0.1, 0.2],
        vehicle_id=requested_id if explicit_vehicle else selected_id,
        top_k=2,
    )
    assert context.get_selected() == selected_id
    assert result == []