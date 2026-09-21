import pytest

from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)
from slm_assistentemanutencaocarro.domain.question_type import QuestionType


@pytest.fixture
def classifier():
    return RuleBasedQuestionClassifier()


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        (
            "Qual óleo usar no motor?",
            QuestionType.OLEO_MOTOR,
        ),
        (
            "Qual oleo o motor utiliza?",
            QuestionType.OLEO_MOTOR,
        ),
        (
            "Qual a pressão correta dos pneus?",
            QuestionType.PRESSAO_PNEUS,
        ),
        (
            "Como devo calibrar os pneus?",
            QuestionType.PRESSAO_PNEUS,
        ),
        (
            "Qual o tamanho do pneu?",
            QuestionType.MEDIDA_PNEUS,
        ),
        (
            "Qual é a medida original dos pneus?",
            QuestionType.MEDIDA_PNEUS,
        ),
        (
            "Quem é o presidente?",
            QuestionType.DESCONHECIDO,
        ),
    ],
)
def test_should_classify_question(
    classifier,
    question,
    expected,
):
    result = classifier.classify(question)

    assert result.question_type == expected