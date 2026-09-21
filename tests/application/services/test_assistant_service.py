from slm_assistentemanutencaocarro.application.ports.vehicle_reader import VehicleReader
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import JsonVehicleReader
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_intent_classifier import RuleBasedIntentClassifier
from slm_assistentemanutencaocarro.config.settings import Settings
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
from slm_assistentemanutencaocarro.application.services.assistant_service import (
    AssistantService,
)
from slm_assistentemanutencaocarro.application.services.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.application.services.vehicle_service import (
    VehicleService,
)

model_name = Settings().ollama_intent_model


def create_assistant(model_name):

    intent_classifier = HybridIntentClassifier(
        rule_based_classifier=RuleBasedIntentClassifier(),
        ollama_classifier=OllamaIntentClassifier(model=model_name)
    )

    question_classifier = RuleBasedQuestionClassifier()

    reader:VehicleReader = JsonVehicleReader("data/vehicle.json")
    vehicle_service = VehicleService(reader)
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

    assistant = create_assistant(model_name)

    result = assistant.answer("Qual óleo usar no motor?")

    assert result == ("O óleo especificado é 5W-30.")


def test_should_answer_tire_pressure_question():

    assistant = create_assistant(model_name)

    result = assistant.answer("Qual a pressão correta dos pneus?")

    assert "33 PSI" in result


def test_should_answer_tire_size_question():

    assistant = create_assistant(model_name)

    result = assistant.answer("Qual o tamanho dos pneus?")

    assert "205/55 R17" in result
