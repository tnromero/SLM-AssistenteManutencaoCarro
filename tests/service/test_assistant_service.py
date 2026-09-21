from slm_assistentemanutencaocarro.config.model_name import OLLAMA_MODEL
from slm_assistentemanutencaocarro.controller.intent_classifier.hybrid_intent_classifier import (
    HybridIntentClassifier,
)
from slm_assistentemanutencaocarro.controller.intent_classifier.ollama_intent_classifier import OllamaIntentClassifier
from slm_assistentemanutencaocarro.controller.question_classifier.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)
from slm_assistentemanutencaocarro.repository.vehicle_repository import (
    VehicleRepository,
)
from slm_assistentemanutencaocarro.service.assistant_service import (
    AssistantService,
)
from slm_assistentemanutencaocarro.service.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.service.vehicle_service import (
    VehicleService,
)


def create_service():

    intent_classifier = HybridIntentClassifier(ollama_model=OllamaIntentClassifier(model=OLLAMA_MODEL.QWEN_3))

    question_classifier = (
        RuleBasedQuestionClassifier()
    )

    repository = VehicleRepository(
        "data/vehicle.json"
    )

    vehicle_service = VehicleService(
        repository
    )

    query_service = VehicleQueryService(
        vehicle_service
    )

    return AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=query_service,
    )


def test_should_answer_oil_question():

    assistant = create_service()

    result = assistant.answer(
        "Qual óleo usar no motor?"
    )

    assert result.answer == (
        "O óleo especificado é 5W-30."
    )


def test_should_answer_tire_pressure_question():

    assistant = create_service()

    result = assistant.answer(
        "Qual a pressão correta dos pneus?"
    )

    assert "33 PSI" in result.answer


def test_should_answer_tire_size_question():

    assistant = create_service()

    result = assistant.answer(
        "Qual o tamanho dos pneus?"
    )

    assert "205/55 R17" in result.answer
