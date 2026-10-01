import csv
import time
from pathlib import Path

from benchmark.model.benchmark_result import BenchmarkResult
from slm_assistentemanutencaocarro.application.ports.question_classifier import QuestionClassifier
from slm_assistentemanutencaocarro.application.ports.response_generator import ResponseGenerator
from slm_assistentemanutencaocarro.application.services.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.application.services.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.application.services.vehicle_service import VehicleService
from slm_assistentemanutencaocarro.config.settings import Settings
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (
    HybridResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (
    OllamaResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_response_generator import (
    RuleBasedResponseGenerator,
)


class ResponseGeneratorBenchmark:
    @staticmethod
    def evaluate(
        evaluate_name: str,
        response_generator: ResponseGenerator,
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

            if expected_answer.lower() in response.lower():
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


def main():
    settings = Settings()

    vehicle_query_service = create_vehicle_query_answer()
    question_classifier = RuleBasedQuestionClassifier()

    rule_generator = RuleBasedResponseGenerator()

    ollama_generator = OllamaResponseGenerator(model=settings.ollama_response_model)

    hybrid_generator = HybridResponseGenerator(
        rule_generator=rule_generator,
        ollama_generator=ollama_generator,
        validator=ResponseValidationService(),
    )

    result = ResponseGeneratorBenchamark.evaluate(
        "Rule Based", rule_generator, vehicle_query_service, question_classifier
    )
    print(result)

    result = ResponseGeneratorBenchamark.evaluate(
        "Ollama", ollama_generator, vehicle_query_service, question_classifier, False
    )
    print(result)

    result = ResponseGeneratorBenchamark.evaluate(
        "Hybrid", hybrid_generator, vehicle_query_service, question_classifier, False
    )
    print(result)


if __name__ == "__main__":
    main()
