from slm_assistentemanutencaocarro.config.settings import OLLAMA_MODEL
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_intent_classifier import (
    HybridIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_intent_classifier import (
    OllamaIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (
    HybridResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (
    OllamaResponseGenerator,
)
from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_response_generator import (
    RuleBasedResponseGenerator,
)
from slm_assistentemanutencaocarro.repository.vehicle_repository import (
    VehicleRepository,
)
from slm_assistentemanutencaocarro.application.services.assistant_service import (
    AssistantService,
)
from slm_assistentemanutencaocarro.application.services.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.application.services.vehicle_service import (
    VehicleService,
)


def create_assistant():

    intent_classifier = HybridIntentClassifier(
        ollama_model=OllamaIntentClassifier(model=OLLAMA_MODEL.QWEN_3)
    )

    question_classifier = RuleBasedQuestionClassifier()

    repository = VehicleRepository("data/vehicle.json")

    vehicle_service = VehicleService(repository)

    query_service = VehicleQueryService(vehicle_service)

    response_generator: ResponseGenerator = HybridResponseGenerator(
        RuleBasedResponseGenerator(), OllamaResponseGenerator()
    )

    return AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=query_service,
        response_generator=response_generator,
    )


def test_should_answer_oil_question():

    assistant = create_assistant()

    result = assistant.answer("Qual óleo usar no motor?")

    assert result == ("O óleo especificado é 5W-30.")


def test_should_answer_tire_pressure_question():

    assistant = create_assistant()

    result = assistant.answer("Qual a pressão correta dos pneus?")

    assert "33 PSI" in result


def test_should_answer_tire_size_question():

    assistant = create_assistant()

    result = assistant.answer("Qual o tamanho dos pneus?")

    assert "205/55 R17" in result
