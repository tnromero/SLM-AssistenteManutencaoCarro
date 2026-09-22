from unittest.mock import Mock, patch

from slm_assistentemanutencaocarro.domain.intent import Intent
from slm_assistentemanutencaocarro.domain.intent_classification import IntentClassification
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_intent_classifier import (
    SYSTEM_PROMPT,
    OllamaIntentClassifier,
)


def test_should_classify_intent():

    response = Mock()
    response.message.content = '{"intent": "Especificação"}'

    with patch(
        "slm_assistentemanutencaocarro.infrastructure.ollama.ollama_intent_classifier.ollama.chat",
        return_value=response,
    ) as chat:
        classifier = OllamaIntentClassifier(model="qwen3:1.7b")

        result = classifier.classify("Qual óleo devo usar?")

    assert result.intent == Intent.ESPECIFICACAO
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
                "content": "Qual óleo devo usar?",
            },
        ],
        format=IntentClassification.model_json_schema(),
    )
