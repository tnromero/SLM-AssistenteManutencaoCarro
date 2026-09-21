from slm_assistentemanutencaocarro.application.ports.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.domain.question_classification import (
    QuestionClassification,
)
from slm_assistentemanutencaocarro.domain.question_type import QuestionType


class HybridQuestionClassifier(QuestionClassifier):
    def __init__(
        self,
        rule_classifier: QuestionClassifier,
        slm_classifier: QuestionClassifier,
    ):
        self.rule_classifier = rule_classifier
        self.slm_classifier = slm_classifier
        self.slm_calls = 0

    def classify(
        self,
        question: str,
    ) -> QuestionClassification:

        rule_result = self.rule_classifier.classify(question)

        if rule_result.question_type != QuestionType.DESCONHECIDO:
            return rule_result

        self.slm_calls += 1
        return self.slm_classifier.classify(question)

    @property
    def slm_call_count(self) -> int:
        return self.slm_calls
