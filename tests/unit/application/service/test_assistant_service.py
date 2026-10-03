from unittest.mock import Mock, call

from slm_assistentemanutencaocarro.application.ports.intent_classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.application.ports.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.application.service.assistant_service import (
    AssistantService,
)
from slm_assistentemanutencaocarro.application.service.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.domain.exception import VehicleDataNotFoundError
from slm_assistentemanutencaocarro.domain.intent import Intent
from slm_assistentemanutencaocarro.domain.intent_classification import IntentClassification
from slm_assistentemanutencaocarro.domain.question_classification import QuestionClassification
from slm_assistentemanutencaocarro.domain.question_type import QuestionType
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


def test_should_answer_specification_question():
    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock(spec=VehicleQueryService)
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.ESPECIFICACAO
    )

    question_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.OLEO_MOTOR
    )

    vehicle_answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )
    vehicle_query_service.answer.return_value = vehicle_answer

    response_generator.generate.return_value = (
        "Para esse veículo, utilize óleo 5W-40."
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual óleo devo usar?")

    assert result == "Para esse veículo, utilize óleo 5W-40."

    response_generator.generate.assert_called_once_with(vehicle_answer)

def test_should_not_continue_when_intent_is_not_supported():
    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock(spec=VehicleQueryService)
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.OUTRO
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual a capital da França?")

    assert result == service.UNSUPPORTED_INTENT_MESSAGE

    question_classifier.classify.assert_not_called()
    vehicle_query_service.answer.assert_not_called()
    response_generator.generate.assert_not_called()

def test_should_not_continue_when_question_type_is_not_supported():
    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock(spec=VehicleQueryService)
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.ESPECIFICACAO
    )

    question_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.DESCONHECIDO
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual o torque do parafuso do suporte do motor?")

    assert result == service.UNSUPPORTED_QUESTION_MESSAGE

    vehicle_query_service.answer.assert_not_called()
    response_generator.generate.assert_not_called()

def test_should_classify_question_before_querying_vehicle():
    orchestration_mock = Mock()

    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock(spec=VehicleQueryService)
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.ESPECIFICACAO
    )

    question_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.OLEO_MOTOR
    )

    vehicle_answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    vehicle_query_service.answer.return_value = vehicle_answer

    response_generator.generate.return_value = (
        "Para esse veículo, utilize óleo 5W-40."
    )

    orchestration_mock.attach_mock(
        intent_classifier,
        "intent_classifier",
    )
    orchestration_mock.attach_mock(
        question_classifier,
        "question_classifier",
    )
    orchestration_mock.attach_mock(
        vehicle_query_service,
        "vehicle_query_service",
    )
    orchestration_mock.attach_mock(
        response_generator,
        "response_generator",
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual óleo devo usar?")

    expected_order = [
        call.intent_classifier.classify(
            "Qual óleo devo usar?"
        ),
        call.question_classifier.classify(
            "Qual óleo devo usar?"
        ),
        call.vehicle_query_service.answer(
            "Qual óleo devo usar?",
            QuestionType.OLEO_MOTOR,
        ),
        call.response_generator.generate(
            vehicle_answer
        ),
    ]

    assert orchestration_mock.mock_calls == expected_order
    assert result == "Para esse veículo, utilize óleo 5W-40."

def test_should_send_vehicle_answer_to_response_generator():
    
    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock(spec=VehicleQueryService)
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.ESPECIFICACAO
    )

    question_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.OLEO_MOTOR
    )

    vehicle_answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    vehicle_query_service.answer.return_value = vehicle_answer

    response_generator.generate.return_value = (
        "Para esse veículo, utilize óleo 5W-40."
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual óleo devo usar?")

    response_generator.generate.assert_called_once_with(vehicle_answer)

    assert result == "Para esse veículo, utilize óleo 5W-40."

def test_should_return_message_when_vehicle_data_is_not_found():
    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock(spec=VehicleQueryService)
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.ESPECIFICACAO
    )

    question_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.OLEO_MOTOR
    )

    vehicle_query_service.answer.side_effect = VehicleDataNotFoundError()

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual óleo devo usar?")

    assert result == service.DATA_NOT_FOUND_MESSAGE

    response_generator.generate.assert_not_called()

def test_should_return_message_when_question_type_is_not_supported():
    intent_classifier = Mock(spec=IntentClassifier)
    question_classifier = Mock(spec=QuestionClassifier)
    vehicle_query_service = Mock(spec=VehicleQueryService)
    response_generator = Mock(spec=ResponseGenerator)

    intent_classifier.classify.return_value = IntentClassification(
        intent=Intent.ESPECIFICACAO
    )

    question_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.DESCONHECIDO
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual a capital da França?")

    assert result == service.UNSUPPORTED_QUESTION_MESSAGE

    vehicle_query_service.answer.assert_not_called()