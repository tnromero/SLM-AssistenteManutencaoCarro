import pytest
from unittest.mock import Mock

from slm_assistentemanutencaocarro.application.ports.question_classifier import QuestionClassifier
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


def test_should_use_rule_classifier_when_question_is_known():
    rule_classifier = Mock(spec=QuestionClassifier)
    slm_classifier = Mock(spec=QuestionClassifier)

    rule_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.OLEO_MOTOR
    )

    classifier = HybridQuestionClassifier(
        rule_classifier=rule_classifier,
        slm_classifier=slm_classifier,
    )

    result = classifier.classify("Qual óleo devo usar?")

    assert result.question_type == QuestionType.OLEO_MOTOR
    slm_classifier.classify.assert_not_called()
    assert classifier.slm_call_count == 0


def test_should_use_slm_when_rule_classifier_returns_unknown():
    rule_classifier = Mock(spec=QuestionClassifier)
    slm_classifier = Mock(spec=QuestionClassifier)

    rule_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.DESCONHECIDO
    )

    slm_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.MEDIDA_PNEUS
    )

    classifier = HybridQuestionClassifier(
        rule_classifier=rule_classifier,
        slm_classifier=slm_classifier,
    )

    result = classifier.classify("Qual pneu devo utilizar nessa situação?")

    assert result.question_type == QuestionType.MEDIDA_PNEUS
    slm_classifier.classify.assert_called_once_with(
        "Qual pneu devo utilizar nessa situação?"
    )
    assert classifier.slm_call_count == 1

def test_should_count_slm_calls():
    rule_classifier = Mock(spec=QuestionClassifier)
    slm_classifier = Mock(spec=QuestionClassifier)

    rule_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.DESCONHECIDO
    )

    slm_classifier.classify.return_value = QuestionClassification(
        question_type=QuestionType.MEDIDA_PNEUS
    )

    classifier = HybridQuestionClassifier(
        rule_classifier=rule_classifier,
        slm_classifier=slm_classifier,
    )

    classifier.classify("Pergunta 1")
    classifier.classify("Pergunta 2")
    classifier.classify("Pergunta 3")

    assert classifier.slm_call_count == 3