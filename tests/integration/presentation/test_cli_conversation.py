from unittest.mock import Mock, patch

import pytest

from slm_assistentemanutencaocarro.application.application import Application
from slm_assistentemanutencaocarro.application.context.conversation_context import (  # noqa: E501
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.exception import (
    KnowledgeReadError,
    RagGenerationError,
    SessionPersistenceError,
)
from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_document import (
    KnowledgeDocument,
)
from slm_assistentemanutencaocarro.application.model.knowledge_search_result import (  # noqa: E501
    KnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.model.rag_answer import RagAnswer
from slm_assistentemanutencaocarro.application.port.vehicle_reader import (
    VehicleReader,
)
from slm_assistentemanutencaocarro.application.service.assistant_service import (  # noqa: E501
    AssistantService,
)
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (  # noqa: E501
    KnowledgeSearchService,
)
from slm_assistentemanutencaocarro.application.service.knowledge_service import (  # noqa: E501
    KnowledgeService,
)
from slm_assistentemanutencaocarro.application.service.rag_service import (
    RagService,
)
from slm_assistentemanutencaocarro.application.service.session_service import (
    SessionService,
)
from slm_assistentemanutencaocarro.domain.exception import (
    VehicleNotFoundError,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.presentation.cli import run


@pytest.fixture
def application():

    session_service = Mock(spec=SessionService)
    session_service.restore.return_value = False

    vehicle_context = VehicleContext()
    vehicle_context.select(VehicleId(value="t-cross-2022"))

    conversation_context = ConversationContext()
    conversation_context.add_turn(
        question="Qual óleo devo usar?",
        response="Utilize óleo 5W-40.",
    )

    knowledge_service = Mock(spec=KnowledgeService)
    knowledge_search_service = Mock(spec=KnowledgeSearchService)
    rag_service = Mock(spec=RagService)

    return Application(
        assistant=Mock(spec=AssistantService),
        vehicle_reader=Mock(spec=VehicleReader),
        vehicle_context=vehicle_context,
        conversation_context=conversation_context,
        session_service=session_service,
        knowledge_service=knowledge_service,
        knowledge_search_service=knowledge_search_service,
        rag_service=rag_service,
    )

@pytest.mark.parametrize(
    ("vehicle_id", "should_clear"),
    [
        ("t-cross-2022", False),
        ("polo-2023", True),
    ],
)
def test_vehicle_selection_updates_history(
    application,
    vehicle_id,
    should_clear,
):
    previous_messages = application.conversation_context.get_messages()

    with patch(
        "builtins.input",
        side_effect=[f"/vehicle {vehicle_id}", "/exit"],
    ):
        run(application)

    assert application.vehicle_context.get_selected() == VehicleId(
        value=vehicle_id,
    )

    expected_messages = () if should_clear else previous_messages

    assert (
        application.conversation_context.get_messages()
        == expected_messages
    )
    application.assistant.answer.assert_not_called()

def test_unknown_vehicle_preserves_session(application):
    previous_vehicle = application.vehicle_context.get_selected()
    previous_messages = application.conversation_context.get_messages()

    application.vehicle_reader.get_vehicle.side_effect = (
        VehicleNotFoundError()
    )

    with patch(
        "builtins.input",
        side_effect=["/vehicle inexistente", "/exit"],
    ):
        run(application)

    assert application.vehicle_context.get_selected() == previous_vehicle
    assert (
        application.conversation_context.get_messages()
        == previous_messages
    )
    application.assistant.answer.assert_not_called()

def test_clear_command_preserves_selected_vehicle(application):
    previous_vehicle = application.vehicle_context.get_selected()

    with patch(
        "builtins.input",
        side_effect=["/cls", "/exit"],
    ):
        run(application)

    assert application.conversation_context.get_messages() == ()
    assert application.vehicle_context.get_selected() == previous_vehicle
    application.assistant.answer.assert_not_called()

def test_save_command(application):
    with patch(
        "builtins.input",
        side_effect=["/save", "/exit"],
    ):
        run(application)

    application.session_service.save.assert_called_once_with()
    application.assistant.answer.assert_not_called()


def test_load_command(application):
    with patch(
        "builtins.input",
        side_effect=["/load", "/exit"],
    ):
        run(application)

    # Uma chamada no início e outra pelo comando.
    assert application.session_service.restore.call_count == 2
    application.assistant.answer.assert_not_called()


def test_restore_failure_allows_cli_to_continue(application, capsys):
    application.session_service.restore.side_effect = (
        SessionPersistenceError("Arquivo inválido")
    )

    with patch(
        "builtins.input",
        side_effect=["/save", "/exit"],
    ):
        run(application)

    assert "Não foi possível restaurar" in capsys.readouterr().out
    application.session_service.save.assert_called_once_with()

def test_saves_after_answer(application):
    application.assistant.answer.return_value = "Utilize óleo 5W-40."

    with patch(
        "builtins.input",
        side_effect=["Qual óleo devo usar?", "/exit"],
    ):
        run(application)

    application.session_service.save.assert_called_once_with()


def test_does_not_save_when_answer_fails(application):
    application.assistant.answer.side_effect = RuntimeError(
        "Falha ao responder"
    )

    with patch(
        "builtins.input",
        side_effect=["Qual óleo devo usar?", "/exit"],
    ):
        run(application)

    application.session_service.save.assert_not_called()


def test_save_failure_preserves_response(application, capsys):
    application.assistant.answer.return_value = "Utilize óleo 5W-40."
    application.session_service.save.side_effect = (
        SessionPersistenceError("Falha na gravação")
    )

    with patch(
        "builtins.input",
        side_effect=["Qual óleo devo usar?", "/exit"],
    ):
        run(application)

    output = capsys.readouterr().out

    assert "Utilize óleo 5W-40." in output
    assert "A sessão não foi salva" in output

def test_lists_documents_without_calling_assistant(application, capsys):
    application.knowledge_service.list_documents.return_value = [
        KnowledgeDocument(
            id="cuidados-pneus",
            title="Cuidados com os pneus",
            content="Conteúdo de teste.",
            source="Material de estudo",
        )
    ]

    with patch(
        "builtins.input",
        side_effect=["/docs", "/exit"],
    ):
        run(application)

    output = capsys.readouterr().out

    assert "cuidados-pneus: Cuidados com os pneus" in output
    assert "Fonte: Material de estudo" in output
    application.assistant.answer.assert_not_called()
    application.session_service.save.assert_not_called()

def test_document_read_failure_allows_cli_to_continue(application, capsys):
    application.knowledge_service.list_documents.side_effect = (
        KnowledgeReadError("Documento inexistente")
    )

    with patch(
        "builtins.input",
        side_effect=["/docs", "/save", "/exit"],
    ):
        run(application)

    assert (
        "Não foi possível listar os documentos"
        in capsys.readouterr().out
    )
    application.session_service.save.assert_called_once_with()

def test_indexes_documents(application, capsys):
    application.knowledge_search_service.build_index.return_value = 2

    with patch(
        "builtins.input",
        side_effect=["/index", "/exit"],
    ):
        run(application)

    application.knowledge_search_service.build_index.assert_called_once_with()
    assert "Índice preparado com 2 chunks" in capsys.readouterr().out
    application.assistant.answer.assert_not_called()
    application.session_service.save.assert_not_called()


def test_searches_documents(application, capsys):
    application.knowledge_search_service.search.return_value = [
        KnowledgeSearchResult(
            chunk=KnowledgeChunk(
                id="pneus:chunk:0",
                document_id="pneus",
                title="Cuidados com os pneus",
                content="Consulte os dados do veículo.",
                source="Material de teste",
                position=0,
            ),
            score=0.8,
        )
    ]

    with patch(
        "builtins.input",
        side_effect=["/search Como consultar a pressão?", "/exit"],
    ):
        run(application)

    application.knowledge_search_service.search.assert_called_once_with(
        question="Como consultar a pressão?",
        top_k=3,
    )

    output = capsys.readouterr().out
    assert "Cuidados com os pneus" in output
    assert "Fonte: Material de teste" in output
    assert "0.8000" in output
    application.assistant.answer.assert_not_called()


def test_search_requires_question(application, capsys):
    with patch(
        "builtins.input",
        side_effect=["/search", "/exit"],
    ):
        run(application)

    application.knowledge_search_service.search.assert_not_called()
    assert "Uso: /search <pergunta>" in capsys.readouterr().out

def test_rag_command_displays_answer_and_references(application, capsys):
    result = KnowledgeSearchResult(
        chunk=KnowledgeChunk(
            id="pneus:chunk:0",
            document_id="pneus",
            title="Cuidados com os pneus",
            content="Consulte os dados do veículo.",
            source="Material de teste",
            position=0,
        ),
        score=0.8,
    )

    application.rag_service.answer.return_value = RagAnswer(
        response="Consulte os dados do veículo [1].",
        results=(result,),
    )

    with patch(
        "builtins.input",
        side_effect=["/rag Onde consultar a pressão?", "/exit"],
    ):
        run(application)

    application.rag_service.answer.assert_called_once_with(
        question="Onde consultar a pressão?",
        top_k=3,
    )

    output = capsys.readouterr().out
    assert "Consulte os dados do veículo [1]." in output
    assert "[1] Cuidados com os pneus" in output
    assert "Fonte: Material de teste" in output

    application.assistant.answer.assert_not_called()
    application.session_service.save.assert_not_called()


def test_rag_requires_question(application, capsys):
    with patch(
        "builtins.input",
        side_effect=["/rag", "/exit"],
    ):
        run(application)

    application.rag_service.answer.assert_not_called()
    assert "Uso: /rag <pergunta>" in capsys.readouterr().out


def test_rag_failure_allows_cli_to_continue(application, capsys):
    application.rag_service.answer.side_effect = RagGenerationError(
        "Ollama indisponível"
    )

    with patch(
        "builtins.input",
        side_effect=["/rag Onde consultar a pressão?", "/save", "/exit"],
    ):
        run(application)

    assert (
        "Não foi possível responder com documentos"
        in capsys.readouterr().out
    )
    application.session_service.save.assert_called_once_with()

def test_unknown_command(application):
    with patch(
        "builtins.input",
        side_effect=["/zxpto", "/exit"],
    ):
        run(application)

    application.assistant.answer.assert_not_called()
    application.rag_service.answer.assert_not_called()
