from unittest.mock import Mock

import pytest

from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.exception import (
    SessionPersistenceError,
)
from slm_assistentemanutencaocarro.application.model.conversation_message import (
    ConversationMessage,
    MessageRole,
)
from slm_assistentemanutencaocarro.application.model.conversation_session import (
    ConversationSession,
)
from slm_assistentemanutencaocarro.application.port.session_repository import (
    SessionRepository,
)
from slm_assistentemanutencaocarro.application.port.vehicle_reader import (
    VehicleReader,
)
from slm_assistentemanutencaocarro.application.service.session_service import (
    SessionService,
)
from slm_assistentemanutencaocarro.domain.exception import VehicleNotFoundError
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


@pytest.fixture
def session_setup():
    repository = Mock(spec=SessionRepository)
    vehicle_reader = Mock(spec=VehicleReader)
    vehicle_context = VehicleContext()
    conversation_context = ConversationContext()

    service = SessionService(
        repository=repository,
        vehicle_reader=vehicle_reader,
        vehicle_context=vehicle_context,
        conversation_context=conversation_context,
    )

    return (
        service,
        repository,
        vehicle_reader,
        vehicle_context,
        conversation_context,
    )

def test_saves_current_state(session_setup):
    service, repository, _, vehicle_context, context = session_setup
    vehicle_id = VehicleId(value="t-cross-2022")

    vehicle_context.select(vehicle_id)
    context.add_turn("Qual óleo?", "5W-40")

    service.save()

    repository.save.assert_called_once_with(
        ConversationSession(
            vehicle_id=vehicle_id,
            messages=context.get_messages(),
        )
    )


def test_restores_saved_state(session_setup):
    service, repository, reader, vehicle_context, context = session_setup

    saved = ConversationSession(
        vehicle_id=VehicleId(value="t-cross-2022"),
        messages=(
            ConversationMessage(MessageRole.USER, "Qual óleo?"),
            ConversationMessage(MessageRole.ASSISTANT, "5W-40"),
        ),
    )
    repository.load.return_value = saved

    assert service.restore() is True
    assert vehicle_context.get_selected() == saved.vehicle_id
    assert context.get_messages() == saved.messages
    reader.get_vehicle.assert_called_once_with(saved.vehicle_id)


def test_missing_session_preserves_current_state(session_setup):
    service, repository, _, vehicle_context, context = session_setup
    vehicle_id = VehicleId(value="t-cross-2022")
    vehicle_context.select(vehicle_id)
    context.add_turn("Qual óleo?", "5W-40")
    previous_messages = context.get_messages()
    repository.load.return_value = None

    assert service.restore() is False
    assert vehicle_context.get_selected() == vehicle_id
    assert context.get_messages() == previous_messages


def test_unknown_vehicle_preserves_current_state(session_setup):
    service, repository, reader, vehicle_context, context = session_setup
    current_id = VehicleId(value="t-cross-2022")
    vehicle_context.select(current_id)
    context.add_turn("Qual óleo?", "5W-40")
    previous_messages = context.get_messages()

    repository.load.return_value = ConversationSession(
        vehicle_id=VehicleId(value="inexistente"),
        messages=(),
    )
    reader.get_vehicle.side_effect = VehicleNotFoundError()

    with pytest.raises(SessionPersistenceError):
        service.restore()

    assert vehicle_context.get_selected() == current_id
    assert context.get_messages() == previous_messages


def test_empty_session_clears_current_state(session_setup):
    service, repository, reader, vehicle_context, context = session_setup
    vehicle_context.select(VehicleId(value="t-cross-2022"))
    context.add_turn("Qual óleo?", "5W-40")

    repository.load.return_value = ConversationSession(
        vehicle_id=None,
        messages=(),
    )

    assert service.restore() is True
    assert vehicle_context.get_selected() is None
    assert context.get_messages() == ()
    reader.get_vehicle.assert_not_called()