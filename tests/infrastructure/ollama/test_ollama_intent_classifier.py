from slm_assistentemanutencaocarro.config.settings import Settings
from slm_assistentemanutencaocarro.domain.intent import Intent
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_intent_classifier import (
    OllamaIntentClassifier,
)

model_name = Settings().ollama_intent_model


def test_ollama_should_classify_intent():
    classifier = OllamaIntentClassifier(model=model_name)

    result = classifier.classify("Quando devo trocar o óleo?")

    assert result.intent.value == Intent.MANUTENCAO


def test_ollama_should_classify_intent_ollama_model_qwen_3_consistency():

    classifier = OllamaIntentClassifier(model=model_name)

    text = "Quando devo trocar o óleo?"

    results = [classifier.classify(text).intent for _ in range(5)]

    assert all(result == Intent.MANUTENCAO for result in results)
