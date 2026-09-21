from slm_assistentemanutencaocarro.controller.intent_classifier.intent_classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.controller.question_classifier.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.controller.response_generator.response_generator import ResponseGenerator
from slm_assistentemanutencaocarro.model.intent.intent import Intent
from slm_assistentemanutencaocarro.service.vehicle_query_service import (
    VehicleQueryService,
)


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

        return self.response_generator.generate(
            vehicle_answer
        )
