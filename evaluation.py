import csv

from slm_assistentemanutencaocarro.config.models import QWEN_3, LLAMA_3_2
from slm_assistentemanutencaocarro.controller.hybrid_intent_classifier import (
    HybridIntentClassifier,
)
from slm_assistentemanutencaocarro.controller.ollama_intent_classifier import (
    OllamaIntentClassifier,
)
from slm_assistentemanutencaocarro.controller.rule_based_intent_classifier import (
    RuleBasedIntentClassifier,
)
from slm_assistentemanutencaocarro.benchmark.intent_classifier_benchmark import (
    IntentClassifierBenchmark,
)
from slm_assistentemanutencaocarro.model.intent_classifier_benchmark_result import (
    IntentClassifierBenchmarkResult,
)


def load_test_cases(
    csv_file_name: str, enconding_file: str = "utf-8", delimiter=","
) -> list[dict[str, str]]:

    test_cases: list[dict[str, str]]
    with open(csv_file_name, encoding=enconding_file) as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        test_cases = list(reader)

    return test_cases


def main():

    for csv_file_name in ["data/intents.csv", "data/generalization.csv"]:
        test_case = load_test_cases(csv_file_name=csv_file_name)

        result: IntentClassifierBenchmarkResult = IntentClassifierBenchmark().evaluate(
            OllamaIntentClassifier(model=QWEN_3), test_case, 
            # HybridIntentClassifier(ollama_model=OllamaIntentClassifier(model=QWEN_3)), test_case,
        )
        result.display("PT")

        print()
        print()
        print("====================================================")


if __name__ == "__main__":
    main()
