from unittest.mock import Mock

from slm_assistentemanutencaocarro.domain.question_classification import (
    QuestionClassification,
)
from slm_assistentemanutencaocarro.domain.question_type import QuestionType
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_question_classifier import (
    HybridQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)


def test_should_use_rule_based_classifier_first():

    rule_classifier = RuleBasedQuestionClassifier()
    slm_classifier = Mock()

    classifier = HybridQuestionClassifier(
        rule_classifier=rule_classifier,
        slm_classifier=slm_classifier,
    )

    result: QuestionClassification = classifier.classify("Qual óleo usar no motor?")

    assert result.question_type == QuestionType.OLEO_MOTOR

    slm_classifier.classify.assert_not_called()


def test_should_use_slm_when_rule_based_classifier_cannot_classify():

    rule_classifier = RuleBasedQuestionClassifier()
    slm_classifier = Mock()

    slm_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.OLEO_MOTOR
    )

    classifier = HybridQuestionClassifier(
        rule_classifier=rule_classifier,
        slm_classifier=slm_classifier,
    )

    result = classifier.classify("Que lubrificante é recomendado?")

    assert result.question_type == QuestionType.OLEO_MOTOR

    slm_classifier.classify.assert_called_once_with("Que lubrificante é recomendado?")
