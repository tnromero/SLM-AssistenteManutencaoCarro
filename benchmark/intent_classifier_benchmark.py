import time

from benchmark.intent_classifier_benchmark_result import IntentClassifierBenchmarkResult
from slm_assistentemanutencaocarro.application.ports.intent_classifier import IntentClassifier


class IntentClassifierBenchmark:
    @staticmethod
    def evaluate(
        evaluate_name: str, intent_classifier: IntentClassifier, test_case: list[dict[str, str]]
    ) -> IntentClassifierBenchmarkResult:

        total = 0
        correct = 0

        start = time.perf_counter()

        for row in test_case:
            result = intent_classifier.classify(row["description"])

            total += 1

            if result.intent.value == row["expected_intent"]:
                correct += 1
            else:
                print(
                    f"ERRO [{evaluate_name}]: "
                    f"{row['description']} | "
                    f"esperado={row['expected_intent']} | "
                    f"obtido={result.intent.value}"
                )

        elapsed = time.perf_counter() - start

        return IntentClassifierBenchmarkResult(
            model=evaluate_name,
            correct=correct,
            total=total,
            elapsed=elapsed,
        )
