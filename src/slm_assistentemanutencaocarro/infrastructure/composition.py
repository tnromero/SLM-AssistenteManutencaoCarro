from slm_assistentemanutencaocarro.application.services.assistant_service import (
    AssistantService,
)
from slm_assistentemanutencaocarro.application.services.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.application.services.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.application.services.vehicle_service import (
    VehicleService,
)
from slm_assistentemanutencaocarro.config.settings import Settings
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_intent_classifier import (
    HybridIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_question_classifier import (
    HybridQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (
    HybridResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_intent_classifier import (
    OllamaIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_classifier import (
    OllamaQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (
    OllamaResponseGenerator,
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


def create_assistant(json_file_vehicle: str) -> AssistantService:

    settings = Settings()

    vehicle_reader = JsonVehicleReader(json_file_vehicle)

    intent_classifier = HybridIntentClassifier(
        rule_based_classifier=RuleBasedIntentClassifier(),
        ollama_classifier=OllamaIntentClassifier(model=settings.ollama_intent_model),
    )

    question_classifier = HybridQuestionClassifier(
        rule_classifier=RuleBasedQuestionClassifier(),
        slm_classifier=OllamaQuestionClassifier(
            model=settings.ollama_question_model
        )
    )

    response_generator =  HybridResponseGenerator(
        rule_generator=RuleBasedResponseGenerator(),
        ollama_generator=OllamaResponseGenerator(
            model=settings.ollama_response_model,
        ),
        validator=ResponseValidationService(),
        use_slm=True
    )

    vehicle_service = VehicleService(vehicle_reader)
    vehicle_query_service = VehicleQueryService(vehicle_service)

    return AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
    )
