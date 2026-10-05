from unittest.mock import Mock, call

import pytest

from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.model.conversation_message import (
    MessageRole,
)
from slm_assistentemanutencaocarro.application.model.intent_classification import (
    IntentClassification,
)
from slm_assistentemanutencaocarro.application.model.question_classification import (
    QuestionClassification,
)
from slm_assistentemanutencaocarro.application.model.vehicle_answer import (
    VehicleAnswer,
)
from slm_assistentemanutencaocarro.application.port.intent_classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.application.port.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.application.port.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.application.service.assistant_service import (
    AssistantService,
)
from slm_assistentemanutencaocarro.application.service.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.domain.intent import Intent
from slm_assistentemanutencaocarro.domain.question_type import QuestionType
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_resolver import (
    RuleBasedQuestionResolver,
)


@pytest.fixture
def conversation_flow():
    context = ConversationContext()

    intent_classifier = Mock(spec=IntentClassifier)
    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.ESPECIFICACAO,
    )

    question_classifier = Mock(spec=QuestionClassifier)
    question_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.OLEO_MOTOR,
    )

    vehicle_query_service = Mock(spec=VehicleQueryService)
    vehicle_query_service.answer.side_effect = lambda question, question_type: VehicleAnswer(
        question=question,
        answer="O óleo especificado é 5W-40.",
    )

    response_generator = Mock(spec=ResponseGenerator)
    response_generator.generate.return_value = "Utilize óleo 5W-40."

    assistant = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
        conversation_context=context,
        question_resolver=RuleBasedQuestionResolver(),
    )

    return assistant, context, intent_classifier, vehicle_query_service


def test_resolves_repeat_and_preserves_original_question(conversation_flow):
    assistant, context, intent_classifier, vehicle_query_service = conversation_flow

    assistant.answer("Qual óleo devo usar?")
    response = assistant.answer("Pode repetir?")

    assert response == "Utilize óleo 5W-40."

    assert intent_classifier.classify.call_args_list == [
        call("Qual óleo devo usar?"),
        call("Qual óleo devo usar?"),
    ]

    assert vehicle_query_service.answer.call_args_list == [
        call("Qual óleo devo usar?", QuestionType.OLEO_MOTOR),
        call("Qual óleo devo usar?", QuestionType.OLEO_MOTOR),
    ]

    assert [message.content for message in context.get_messages()] == [
        "Qual óleo devo usar?",
        "Utilize óleo 5W-40.",
        "Pode repetir?",
        "Utilize óleo 5W-40.",
    ]

def test_cleared_history_does_not_resolve_previous_question(conversation_flow):
    assistant, context, intent_classifier, _ = conversation_flow

    assistant.answer("Qual óleo devo usar?")
    context.clear()

    assistant.answer("Pode repetir?")

    intent_classifier.classify.assert_called_with("Pode repetir?")

    assert [
        message.content
        for message in context.get_messages()
        if message.role == MessageRole.USER
    ] == ["Pode repetir?"]
