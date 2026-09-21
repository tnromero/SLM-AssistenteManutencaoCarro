from slm_assistentemanutencaocarro.controller.hybrid_intent_classifier import (
    HybridIntentClassifier,
)
from slm_assistentemanutencaocarro.model.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.service.vehicle_query_service import (
    VehicleQueryService,
)


class AssistantService:

    def __init__(
        self,
        classifier: HybridIntentClassifier,
        query_service: VehicleQueryService,
    ):
        self.classifier = classifier
        self.query_service = query_service

    def answer(self, question: str) -> VehicleAnswer:
        classification = self.classifier.classify(question)

        return self.query_service.answer(
            question,
            classification.intent,
        )