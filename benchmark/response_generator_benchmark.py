import time

from benchmark.benchmark_result import BenchmarkResult
from slm_assistentemanutencaocarro.application.ports.response_generator import ResponseGenerator
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class ResponseGeneratorBenchamark:

    @staticmethod
    def evaluate(
        evaluate_name: str, response_generator: ResponseGenerator, test_case: list[dict[str, str]]
    ):

        total = 0
        correct = 0

        start = time.perf_counter()

        for row in test_case:
            answer = VehicleAnswer(
                question=row['question'],
                answer=row['expected_answer'],
            )
            result = response_generator.generate(answer)

            total += 1

            if row['expected_answer'] in result:
                correct += 1
            else:
                print(
                    f"ERRO [{evaluate_name}]: "
                    f"{row['question']} | "
                    f"esperado={row['expected_answer']} | "
                    f"obtido={result}"
                )

        elapsed = time.perf_counter() - start

        return BenchmarkResult(
            model=evaluate_name,
            correct=correct,
            total=total,
            elapsed=elapsed,
        )