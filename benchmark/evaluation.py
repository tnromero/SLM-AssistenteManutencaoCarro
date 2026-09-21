import csv

from benchmark.intent_classifier_benchmark import IntentClassifierBenchmark
from benchmark.intent_classifier_benchmark_result import (
    IntentClassifierBenchmarkResult,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_intent_classifier import (
    HybridIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_intent_classifier import (
    OllamaIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_intent_classifier import (
    RuleBasedIntentClassifier,
)

# Modelos
QWEN_3 = "qwen3:1.7b"
LLAMA_3_2 = "llama3.2:1b"

# Arquivos de testes/treinamentos
csv_files = [
    "benchmark/data/intents.csv",
    "benchmark/data/intents_generalization.csv",
]


def load_test_cases(
    csv_file_name: str, enconding_file: str = "utf-8", delimiter=","
) -> list[dict[str, str]]:

    test_cases: list[dict[str, str]]
    with open(csv_file_name, encoding=enconding_file) as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        test_cases = list(reader)

    return test_cases


def main():

    for csv_file_name in csv_files:
        test_case = load_test_cases(csv_file_name=csv_file_name)

        result: IntentClassifierBenchmarkResult = IntentClassifierBenchmark().evaluate(
            "QWEN_3",
            OllamaIntentClassifier(model=QWEN_3),
            test_case,
        )

        result: IntentClassifierBenchmarkResult = IntentClassifierBenchmark().evaluate(
            "Hibrido",
            HybridIntentClassifier(
                rule_based_classifier=RuleBasedIntentClassifier(),
                ollama_classifier=OllamaIntentClassifier(model=QWEN_3),
            ),
            test_case,
        )
        result.display("PT")

        print()
        print()
        print("====================================================")


if __name__ == "__main__":
    main()
