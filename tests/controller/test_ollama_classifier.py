from slm_assistentemanutencaocarro.controller.ollama_classifier import (
    OllamaIntentClassifier,
)


def test_ollama_should_classify_intent():
    classifier = OllamaIntentClassifier()

    result = classifier.classify(
        "Quando devo trocar o óleo?"
    )

    assert result.intent.value == "Manutenção"