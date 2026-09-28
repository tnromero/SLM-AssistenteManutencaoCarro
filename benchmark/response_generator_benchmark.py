import csv
import time
from pathlib import Path

from benchmark.benchmark_result import BenchmarkResult
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

DATASET = Path("benchmark/data/responses.csv")
VEHICLE_FILE = Path("data/vehicle.json")


def load_dataset() -> list[dict]:
    with DATASET.open(encoding="utf-8") as file:
        return list(csv.DictReader(file))


def create_vehicle_query_answer() -> VehicleQueryService:
    vehicle_reader = JsonVehicleReader(str(VEHICLE_FILE))
    vehicle_service = VehicleService(vehicle_reader)

    return VehicleQueryService(vehicle_service)


class ResponseGeneratorBenchamark:
    @staticmethod
    def evaluate(
        evaluate_name: str,
        response_generator: ResponseGenerator,
        vehicle_query_service: VehicleQueryService,
        question_classifier: QuestionClassifier,
        verbose:bool = True
    ) -> BenchmarkResult:
        dataset = load_dataset()

        correct = 0
        total_time = 0.0

        for row in dataset:
            question = row["question"]
            expected_answer = row["expected_answer"]

            question_type = question_classifier.classify(question).question_type

            vehicle_answer = vehicle_query_service.answer(
                question,
                question_type,
            )

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
            model=evaluate_name, correct=correct, total=len(dataset), elapsed=total_time
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
        use_slm=True,
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
