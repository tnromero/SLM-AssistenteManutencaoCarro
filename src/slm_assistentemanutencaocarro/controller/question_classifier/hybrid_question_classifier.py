from slm_assistentemanutencaocarro.controller.question_classifier.ollama_question_classifier import (
    OllamaQuestionClassifier,
)
from slm_assistentemanutencaocarro.controller.question_classifier.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.controller.question_classifier.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)
from slm_assistentemanutencaocarro.model.question.question_classification import (
    QuestionClassification,
)
from slm_assistentemanutencaocarro.model.question.question_type import QuestionType


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
    def slm_call_rate(self) -> float:
        return self.slm_calls