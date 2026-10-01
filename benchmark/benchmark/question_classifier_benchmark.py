import time

from benchmark.model.benchmark_result import BenchmarkResult
from slm_assistentemanutencaocarro.application.ports.question_classifier import (
    QuestionClassifier,
)


class QuestionClassifierBenchmark:
    @staticmethod
    def evaluate(
        evaluate_name: str,
        question_classifier: QuestionClassifier,
        dataset: list[dict[str, str]],
    ) -> BenchmarkResult:
        total = 0
        correct = 0

        start = time.perf_counter()

        for row in dataset:
            result = question_classifier.classify(row["question"])

            total += 1

            if result.question_type.value == row["expected"]:
                correct += 1
            else:
                print(
                    f"ERRO [{evaluate_name}]: "
                    f"{row['question']} | "
                    f"esperado={row['expected']} | "
                    f"obtido={result.question_type.value}"
                )

        elapsed = time.perf_counter() - start

        return BenchmarkResult(
            model=evaluate_name,
            correct=correct,
            total=total,
            elapsed=elapsed,
        )