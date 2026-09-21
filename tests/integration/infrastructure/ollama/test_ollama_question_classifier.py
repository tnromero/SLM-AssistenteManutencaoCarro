import pytest

from slm_assistentemanutencaocarro.config.settings import Settings
from slm_assistentemanutencaocarro.domain.question_type import QuestionType
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_classifier import (
    OllamaQuestionClassifier,
)

model_name = Settings().ollama_response_model

@pytest.fixture
def classifier():
    return OllamaQuestionClassifier(model=model_name)


@pytest.mark.integration
@pytest.mark.parametrize(
    ("question", "expected"),
    [
        (
            "Qual óleo usar no motor?",
            QuestionType.OLEO_MOTOR,
        ),
        (
            "Qual a viscosidade do óleo?",
            QuestionType.OLEO_MOTOR,
        ),
        (
            "Qual a pressão correta dos pneus?",
            QuestionType.PRESSAO_PNEUS,
        ),
        (
            "Quantos PSI devo colocar nos pneus?",
            QuestionType.PRESSAO_PNEUS,
        ),
        (
            "Qual o tamanho dos pneus?",
            QuestionType.MEDIDA_PNEUS,
        ),
        (
            "Qual a medida original dos pneus?",
            QuestionType.MEDIDA_PNEUS,
        ),
    ],
)
def test_should_classify_question(
    classifier: OllamaQuestionClassifier,
    question: str,
    expected: QuestionType,
):
    result = classifier.classify(question)

    assert result.question_type == expected
