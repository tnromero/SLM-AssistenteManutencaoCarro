from unittest.mock import Mock, patch

import pytest

from slm_assistentemanutencaocarro.application.application import Application
from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.port.vehicle_reader import (
    VehicleReader,
)
from slm_assistentemanutencaocarro.application.service.assistant_service import (
    AssistantService,
)
from slm_assistentemanutencaocarro.domain.exception import (
    VehicleNotFoundError,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.presentation.cli import run


@pytest.fixture
def application():
    vehicle_context = VehicleContext()
    vehicle_context.select(VehicleId(value="t-cross-2022"))

    conversation_context = ConversationContext()
    conversation_context.add_turn(
        question="Qual óleo devo usar?",
        response="Utilize óleo 5W-40.",
    )

    return Application(
        assistant=Mock(spec=AssistantService),
        vehicle_reader=Mock(spec=VehicleReader),
        vehicle_context=vehicle_context,
        conversation_context=conversation_context,
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
