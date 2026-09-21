from slm_assistentemanutencaocarro.controller.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.model.question_classification import (
    QuestionClassification,
)
from slm_assistentemanutencaocarro.model.question_type import QuestionType


class RuleBasedQuestionClassifier(QuestionClassifier):

    def classify(
        self,
        question: str,
    ) -> QuestionClassification:

        text = question.lower()

        if "óleo" in text or "oleo" in text:
            return QuestionClassification(
                question_type=QuestionType.OLEO_MOTOR
            )

        if (
            "pressão" in text
            or "pressao" in text
            or "calibr" in text
        ) and "pneu" in text:
            return QuestionClassification(
                question_type=QuestionType.PRESSAO_PNEUS
            )

        if "pneu" in text and (
            "tamanho" in text
            or "medida" in text
        ):
            return QuestionClassification(
                question_type=QuestionType.MEDIDA_PNEUS
            )

        return QuestionClassification(
            question_type=QuestionType.DESCONHECIDO
        )