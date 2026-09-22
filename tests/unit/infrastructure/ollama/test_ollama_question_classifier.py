from unittest.mock import Mock, patch

from slm_assistentemanutencaocarro.domain.question_classification import QuestionClassification
from slm_assistentemanutencaocarro.domain.question_type import QuestionType
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_classifier import (
    SYSTEM_PROMPT,
    OllamaQuestionClassifier,
)


def test_should_classify_question():

    response = Mock()
    response.message.content = '{"question_type": "Óleo do motor"}'

    with patch(
        "slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_classifier.ollama.chat",
        return_value=response,
    ) as chat:
        classifier = OllamaQuestionClassifier(model="qwen3:1.7b")

        result = classifier.classify("Qual óleo usar no motor?")

    assert result.question_type == QuestionType.OLEO_MOTOR
    chat.assert_called_once_with(
        model="qwen3:1.7b",
        think=False,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": "Qual óleo usar no motor?",
            },
        ],
        format=QuestionClassification.model_json_schema(),
    )
