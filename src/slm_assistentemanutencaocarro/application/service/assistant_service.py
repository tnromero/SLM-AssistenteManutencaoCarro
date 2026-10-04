from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.port.intent_classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.application.port.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.application.port.response_generator import ResponseGenerator
from slm_assistentemanutencaocarro.application.service.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.domain.exception import VehicleDataNotFoundError
from slm_assistentemanutencaocarro.domain.intent import Intent
from slm_assistentemanutencaocarro.domain.question_type import QuestionType


class AssistantService:
    UNSUPPORTED_INTENT_MESSAGE = "Ainda não tenho suporte para responder esse tipo de pergunta."

    UNSUPPORTED_QUESTION_MESSAGE = (
        "Ainda não tenho informações para responder essa pergunta sobre o veículo."
    )

    DATA_NOT_FOUND_MESSAGE = "Não encontrei essa informação nos dados disponíveis do veículo."

    def __init__(
        self,
        intent_classifier: IntentClassifier,
        question_classifier: QuestionClassifier,
        vehicle_query_service: VehicleQueryService,
        response_generator: ResponseGenerator,
        conversation_context: ConversationContext,
    ):
        self.intent_classifier = intent_classifier
        self.question_classifier = question_classifier
        self.vehicle_query_service = vehicle_query_service
        self.response_generator = response_generator
        self.conversation_context = conversation_context

    def _answer(self, question: str):

        intent_classification = self.intent_classifier.classify(question)

        if intent_classification.intent != Intent.ESPECIFICACAO:
            return self.UNSUPPORTED_INTENT_MESSAGE

        question_classification = self.question_classifier.classify(question)

        if question_classification.question_type == QuestionType.DESCONHECIDO:
            return self.UNSUPPORTED_QUESTION_MESSAGE

        try:
            vehicle_answer = self.vehicle_query_service.answer(
                question,
                question_classification.question_type,
            )
        except VehicleDataNotFoundError:
            return self.DATA_NOT_FOUND_MESSAGE

        return self.response_generator.generate(vehicle_answer)

    def answer(self, question: str) -> str:
        response = self._answer(question)

        self.conversation_context.add_turn(
            question=question,
            response=response,
        )

        return response
