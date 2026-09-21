from slm_assistentemanutencaocarro.config.models import QWEN_3
from slm_assistentemanutencaocarro.controller.hybrid_intent_classifier import (
    HybridIntentClassifier,
)
from slm_assistentemanutencaocarro.controller.ollama_intent_classifier import OllamaIntentClassifier
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


def create_service() -> AssistantService:
    classifier = HybridIntentClassifier(ollama_model=OllamaIntentClassifier(model=QWEN_3))

    repository = VehicleRepository("data/vehicle.json")

    vehicle_service = VehicleService(repository)

    query_service = VehicleQueryService(
        vehicle_service
    )

    return AssistantService(
        classifier,
        query_service,
    )


def test_should_answer_oil_question():
    service = create_service()

    result = service.answer(
        "Qual óleo usar no motor?"
    )

    assert "5W-30" in result.answer


def test_should_answer_tire_question():
    service = create_service()

    result = service.answer(
        "Qual a pressão correta dos pneus?"
    )

    assert "33 PSI" in result.answer


def test_should_answer_tire_size_question():
    service = create_service()

    result = service.answer(
        "Qual o tamanho do pneu?"
    )

    assert "205/55 R17" in result.answer