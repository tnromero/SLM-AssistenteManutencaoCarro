import time

from slm_assistentemanutencaocarro.controller.intent_classifier import IntentClassifier
from slm_assistentemanutencaocarro.model.intent_classifier_benchmark_result import IntentClassifierBenchmarkResult


class IntentClassifierBenchmark:

    @staticmethod
    def evaluate(intent_classifier: IntentClassifier, test_case: list[dict[str,str]]) -> IntentClassifierBenchmarkResult:

        total = 0
        correct = 0

        intent_classifier.start_classifier()

        start = time.perf_counter()

        for row in test_case:
            result = intent_classifier.classify(row["description"])

            total += 1

            if result.intent.value == row["expected_intent"]:
                correct += 1
            else:
                print(
                    f"ERRO [{intent_classifier.get_model_name()}]: "
                    f"{row['description']} | "
                    f"esperado={row['expected_intent']} | "
                    f"obtido={result.intent.value}"
                )

        elapsed = time.perf_counter() - start

        intent_classifier.close_classifier()

        return IntentClassifierBenchmarkResult(
            model=intent_classifier.get_model_name(),
            correct=correct,
            total=total,
            elapsed=elapsed,
        )
