from slm_assistentemanutencaocarro.application.ports.intent_classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.application.ports.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.application.ports.response_generator import ResponseGenerator
from slm_assistentemanutencaocarro.application.services.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.domain.intent import Intent


class AssistantService:
    def __init__(
        self,
        intent_classifier: IntentClassifier,
        question_classifier: QuestionClassifier,
        vehicle_query_service: VehicleQueryService,
        response_generator: ResponseGenerator,
    ):
        self.intent_classifier = intent_classifier
        self.question_classifier = question_classifier
        self.vehicle_query_service = vehicle_query_service
        self.response_generator = response_generator

    def answer(self, question: str):

        intent = self.intent_classifier.classify(question).intent

        if intent != Intent.ESPECIFICACAO:
            return "Ainda não tenho suporte para responder esse tipo de pergunta."

        question_type = self.question_classifier.classify(question).question_type

        vehicle_answer = self.vehicle_query_service.answer(
            question,
            question_type,
        )

        return self.response_generator.generate(vehicle_answer)
