from benchmark.benchmark.intent_classifier_benchmark import (
    IntentClassifierBenchmark,
)
from benchmark.dataset_loader import DatasetLoader
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_intent_classifier import (
    OllamaIntentClassifier,
)

QWEN_3 = "qwen3:1.7b"
LLAMA_3_2 = "llama3.2:1b"

def main():
    dataset = DatasetLoader().load("intents.csv")

    classifier = OllamaIntentClassifier(
        model=QWEN_3,
    )

    result = IntentClassifierBenchmark.evaluate(
        "QWEN_3",
        classifier,
        dataset,
    )

    print(result)


if __name__ == "__main__":
    main()