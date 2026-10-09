from unittest.mock import Mock

from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.port.vehicle_reader import (
    VehicleReader,
)
from slm_assistentemanutencaocarro.application.service.session_service import (
    SessionService,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.persistence.json_session_repository import (
    JsonSessionRepository,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_resolver import (
    RuleBasedQuestionResolver,
)


def test_restores_context_for_question_resolution(tmp_path):
    path = tmp_path / "session.json"
    vehicle_id = VehicleId(value="t-cross-2022")
    vehicle_reader = Mock(spec=VehicleReader)

    first_vehicle_context = VehicleContext()
    first_vehicle_context.select(vehicle_id)

    first_conversation_context = ConversationContext()
    first_conversation_context.add_turn(
        "Qual óleo devo usar?",
        "Utilize óleo 5W-40.",
    )

    first_service = SessionService(
        repository=JsonSessionRepository(path),
        vehicle_reader=vehicle_reader,
        vehicle_context=first_vehicle_context,
        conversation_context=first_conversation_context,
    )
    first_service.save()

    # Nova instância de cada componente de estado e persistência.
    restored_vehicle_context = VehicleContext()
    restored_conversation_context = ConversationContext()

    restored_service = SessionService(
        repository=JsonSessionRepository(path),
        vehicle_reader=vehicle_reader,
        vehicle_context=restored_vehicle_context,
        conversation_context=restored_conversation_context,
    )

    assert restored_service.restore() is True
    assert restored_vehicle_context.get_selected() == vehicle_id

    resolved_question = RuleBasedQuestionResolver().resolve(
        question="Pode repetir?",
        history=restored_conversation_context.get_messages(),
    )

    assert resolved_question == "Qual óleo devo usar?"
    assert (
        restored_conversation_context.get_messages()
        == first_conversation_context.get_messages()
    )
