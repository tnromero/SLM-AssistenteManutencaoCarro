import csv

from slm_assistentemanutencaocarro.config.models import QWEN_3, LLAMA_3_2
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

    test_case = load_test_cases(csv_file_name="data/intents.csv")

    result_rule_based: IntentClassifierBenchmarkResult = (
        IntentClassifierBenchmark().evaluate(RuleBasedIntentClassifier(), test_case)
    )
    result_rule_based.display("PT")

    result_ollama: IntentClassifierBenchmarkResult = (
        IntentClassifierBenchmark().evaluate(
            OllamaIntentClassifier(model=QWEN_3), test_case
        )
    )
    result_ollama.display("PT")

    result_llama: IntentClassifierBenchmarkResult = IntentClassifierBenchmark().evaluate(OllamaIntentClassifier(model=LLAMA_3_2), test_case)
    result_llama.display("PT")


if __name__ == "__main__":
    main()
