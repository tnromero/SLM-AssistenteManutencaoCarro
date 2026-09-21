from unittest.mock import Mock

from slm_assistentemanutencaocarro.application.ports.intent_classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.application.ports.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.application.services.assistant_service import (
    AssistantService,
)
from slm_assistentemanutencaocarro.domain.intent import Intent
from slm_assistentemanutencaocarro.domain.intent_classification import (
    IntentClassification,
)
from slm_assistentemanutencaocarro.domain.question_classification import (
    QuestionClassification,
)
from slm_assistentemanutencaocarro.domain.question_type import QuestionType
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


def test_should_answer_vehicle_specification_question():
    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock()
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.ESPECIFICACAO
    )

    question_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.OLEO_MOTOR
    )

    vehicle_query_service.answer.return_value = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-30.",
    )

    response_generator.generate.return_value = "O óleo especificado é 5W-30."

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual óleo devo usar?")

    assert result == "O óleo especificado é 5W-30."

def test_should_orchestrate_vehicle_specification_question():
    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock()
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.ESPECIFICACAO
    )

    question_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.OLEO_MOTOR
    )

    vehicle_query_service.answer.return_value = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-30.",
    )

    response_generator.generate.return_value = "O óleo especificado é 5W-30."

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    service.answer("Qual óleo devo usar?")

    intent_classifier.classify.assert_called_once_with(
        "Qual óleo devo usar?"
    )

    question_classifier.classify.assert_called_once_with(
        "Qual óleo devo usar?"
    )

    vehicle_query_service.answer.assert_called_once_with(
        "Qual óleo devo usar?",
        QuestionType.OLEO_MOTOR,
    )

    response_generator.generate.assert_called_once_with(
        vehicle_query_service.answer.return_value
    )

def test_should_reject_unsupported_intent():
    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock()
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.MANUTENCAO
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Quando devo trocar o óleo?")

    assert result == "Ainda não tenho suporte para responder esse tipo de pergunta."

    question_classifier.classify.assert_not_called()
    vehicle_query_service.answer.assert_not_called()
    response_generator.generate.assert_not_called()