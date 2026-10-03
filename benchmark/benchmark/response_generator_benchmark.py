import time

from benchmark.model.benchmark_result import BenchmarkResult
from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.application.services.response_validation_service import ResponseValidationService
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class ResponseGeneratorBenchmark:
    @staticmethod
    def evaluate(
        evaluate_name: str,
        response_generator: ResponseGenerator,
        response_validator: ResponseValidationService,
        dataset: list[dict[str, str]],
        verbose: bool = True,
    ) -> BenchmarkResult:

        correct = 0
        total_time = 0.0

        for row in dataset:
            question = row["question"]
            expected_answer = row["expected_answer"]

            vehicle_answer = VehicleAnswer(question=question, answer=expected_answer)

            start = time.perf_counter()

            response = response_generator.generate(vehicle_answer)

            elapsed = time.perf_counter() - start
            total_time += elapsed

            is_valid = response_validator.validate(
                answer=vehicle_answer, response=response
            )

            if is_valid:
                correct += 1
                status = "✓"
            else:
                status = "✗"

            if verbose:
                print(f"\n{evaluate_name}")
                print(f"{status}         : {question}")
                print(f"  Esperado: {expected_answer}")
                print(f"  Resposta: {response}")
                print(f"  Tempo:    {elapsed}s")

        return BenchmarkResult(
            model=evaluate_name,
            correct=correct,
            total=len(dataset),
            elapsed=total_time
        )
