from slm_assistentemanutencaocarro.controller.intent_classifier.hybrid_intent_classifier import (
    HybridIntentClassifier,
)
from slm_assistentemanutencaocarro.controller.question_classifier.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.model.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.service.vehicle_query_service import (
    VehicleQueryService,
)


class AssistantService:

    def __init__(
        self,
        intent_classifier: HybridIntentClassifier,
        question_classifier: QuestionClassifier,
        query_service: VehicleQueryService,
    ):
        self.intent_classifier = intent_classifier
        self.question_classifier = question_classifier
        self.query_service = query_service

    def answer(self, question: str) -> VehicleAnswer:

        intent = self.intent_classifier.classify(
            question
        ).intent

        question_type = self.question_classifier.classify(
            question
        ).question_type

        return self.query_service.answer(
            question,
            question_type,
        )