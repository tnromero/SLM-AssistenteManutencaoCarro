from unittest.mock import MagicMock, Mock

from slm_assistentemanutencaocarro.application.context.vehicle_context import VehicleContext
from slm_assistentemanutencaocarro.application.ports.response_generator import ResponseGenerator
from slm_assistentemanutencaocarro.application.service.assistant_service import AssistantService
from slm_assistentemanutencaocarro.application.service.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.application.service.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.application.service.vehicle_service import VehicleService
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (
    HybridResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_intent_classifier import (
    RuleBasedIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_response_generator import (
    RuleBasedResponseGenerator,
)


def test_should_answer_using_hybrid_response_generator():

    intent_classifier = RuleBasedIntentClassifier()
    question_classifier = RuleBasedQuestionClassifier()

    vehicle_reader = JsonVehicleReader("data/vehicle.json")

    tcross_id = VehicleId(value="t-cross-2022")
    vehicle_context = VehicleContext()
    vehicle_context.select(tcross_id)

    vehicle_service = VehicleService(vehicle_reader, vehicle_context)

    vehicle_query_service = VehicleQueryService(vehicle_service)

    slm_response_generator = Mock(spec=ResponseGenerator)
    fallback_response_generator = RuleBasedResponseGenerator()
    response_validator = ResponseValidationService()

    slm_response_generator.generate.return_value = "Para esse veículo, utilize óleo 5W-40."

    response_generator = HybridResponseGenerator(
        response_generator=slm_response_generator,
        fallback_generator=fallback_response_generator,
        response_validator=response_validator,
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual óleo devo usar?")

    assert result == "Para esse veículo, utilize óleo 5W-40."
    slm_response_generator.generate.assert_called_once()


def test_should_use_fallback_when_slm_response_is_factually_invalid():

    intent_classifier = RuleBasedIntentClassifier()
    question_classifier = RuleBasedQuestionClassifier()

    vehicle_reader = JsonVehicleReader("data/vehicle.json")
    tcross_id = VehicleId(value="t-cross-2022")
    vehicle_context = VehicleContext()
    vehicle_context.select(tcross_id)

    vehicle_service = VehicleService(vehicle_reader, vehicle_context)

    vehicle_query_service = VehicleQueryService(vehicle_service)

    slm_response_generator = Mock(spec=ResponseGenerator)
    fallback_response_generator = RuleBasedResponseGenerator()
    response_validator = ResponseValidationService()

    slm_response_generator.generate.return_value = "Para esse veículo, utilize óleo 5W-04."

    fallback_response_generator.generate = MagicMock(wraps=fallback_response_generator.generate)

    response_generator = HybridResponseGenerator(
        response_generator=slm_response_generator,
        fallback_generator=fallback_response_generator,
        response_validator=response_validator,
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual óleo devo usar?")

    slm_response_generator.generate.assert_called_once()

    generated_answer = slm_response_generator.generate.call_args.args[0]

    fallback_response_generator.generate.assert_called_once_with(generated_answer)

    assert result == "O óleo especificado é 5W-40."


def test_should_use_fallback_when_slm_raises_exception():

    intent_classifier = RuleBasedIntentClassifier()
    question_classifier = RuleBasedQuestionClassifier()

    vehicle_reader = JsonVehicleReader("data/vehicle.json")
    tcross_id = VehicleId(value="t-cross-2022")
    vehicle_context = VehicleContext()
    vehicle_context.select(tcross_id)

    vehicle_service = VehicleService(vehicle_reader, vehicle_context)

    vehicle_query_service = VehicleQueryService(vehicle_service)

    slm_response_generator = Mock(spec=ResponseGenerator)
    fallback_response_generator = RuleBasedResponseGenerator()
    response_validator = ResponseValidationService()

    slm_response_generator.generate.side_effect = RuntimeError("Ollama indisponível")

    fallback_response_generator.generate = MagicMock(wraps=fallback_response_generator.generate)

    response_generator = HybridResponseGenerator(
        response_generator=slm_response_generator,
        fallback_generator=fallback_response_generator,
        response_validator=response_validator,
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual óleo devo usar?")

    slm_response_generator.generate.assert_called_once()

    generated_answer = slm_response_generator.generate.call_args.args[0]

    fallback_response_generator.generate.assert_called_once_with(generated_answer)

    assert result == "O óleo especificado é 5W-40."


def test_should_reject_question_outside_vehicle_domain():

    intent_classifier = RuleBasedIntentClassifier()
    question_classifier = RuleBasedQuestionClassifier()

    vehicle_reader = JsonVehicleReader("data/vehicle.json")
    tcross_id = VehicleId(value="t-cross-2022")
    vehicle_context = VehicleContext()
    vehicle_context.select(tcross_id)

    vehicle_service = VehicleService(vehicle_reader, vehicle_context)

    vehicle_query_service = VehicleQueryService(vehicle_service)

    slm_response_generator = Mock(spec=ResponseGenerator)
    fallback_response_generator = RuleBasedResponseGenerator()
    response_validator = ResponseValidationService()

    response_generator = HybridResponseGenerator(
        response_generator=slm_response_generator,
        fallback_generator=fallback_response_generator,
        response_validator=response_validator,
    )

    service = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )

    result = service.answer("Qual a capital da França?")

    assert result == (service.UNSUPPORTED_QUESTION_MESSAGE)
