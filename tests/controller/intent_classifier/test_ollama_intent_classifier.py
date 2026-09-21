from slm_assistentemanutencaocarro.config.settings import OLLAMA_MODEL
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_intent_classifier import (
    OllamaIntentClassifier,
)


def test_ollama_should_classify_intent():
    classifier = OllamaIntentClassifier(model=OLLAMA_MODEL.QWEN_3)

    result = classifier.classify(
        "Quando devo trocar o óleo?"
    )

    assert result.intent.value == "Manutenção"

def test_ollama_should_classify_intent_ollama_model_qwen_3_consistency():

    classifier = OllamaIntentClassifier(model=OLLAMA_MODEL.QWEN_3)

    text = "Quando devo trocar o óleo?"

    results = [
        classifier.classify(text).intent.value
        for _ in range(5)
    ]

    assert all(result == "Manutenção" for result in results)