from benchmark.benchmark.response_generator_benchmark import ResponseGeneratorBenchmark
from benchmark.dataset_loader import DatasetLoader
from slm_assistentemanutencaocarro.application.services.response_validation_service import ResponseValidationService
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (
    OllamaResponseGenerator,
)

QWEN_3 = "qwen3:1.7b"

def main():
    loader = DatasetLoader()

    dataset = loader.load("responses.csv")

    response_generator = OllamaResponseGenerator(QWEN_3)

    response_validator = ResponseValidationService()

    result = ResponseGeneratorBenchmark.evaluate(
        evaluate_name="QWEN_3",
        response_generator=response_generator,
        response_validator=response_validator,
        dataset=dataset,
    )

    result.display("PT")


if __name__ == "__main__":
    main()