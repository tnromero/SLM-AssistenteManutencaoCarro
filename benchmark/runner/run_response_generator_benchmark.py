from benchmark.benchmark.response_generator_benchmark import (
    ResponseGeneratorBenchmark,
)
from benchmark.dataset_loader import DatasetLoader
from benchmark.model.benchmark_result import BenchmarkResult
from slm_assistentemanutencaocarro.application.service.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (
    HybridResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (
    OllamaResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_response_generator import (
    RuleBasedResponseGenerator,
)

MODELS = [
    "qwen3:1.7b",
    "llama3.2:1b",
]

DIV_LINE = "=" * 50


def run_ollama_benchmark(
    model_name: str,
    dataset: list[dict[str, str]],
) -> BenchmarkResult:
    response_generator = OllamaResponseGenerator(model_name)

    result = ResponseGeneratorBenchmark.evaluate(
        evaluate_name=model_name,
        response_generator=response_generator,
        response_validator=ResponseValidationService(),
        dataset=dataset,
        verbose=False,
    )

    result = result.model_copy(
        update={
            "strategy": "Ollama",
        }
    )

    return result


def run_hybrid_benchmark(
    model_name: str,
    dataset: list[dict[str, str]],
) -> BenchmarkResult:
    slm_generator = OllamaResponseGenerator(model_name)

    hybrid_generator = HybridResponseGenerator(
        response_generator=slm_generator,
        fallback_generator=RuleBasedResponseGenerator(),
        response_validator=ResponseValidationService(),
    )

    result = ResponseGeneratorBenchmark.evaluate(
        evaluate_name=model_name,
        response_generator=hybrid_generator,
        response_validator=ResponseValidationService(),
        dataset=dataset,
        verbose=False,
    )

    metrics = hybrid_generator.get_metrics()

    result = result.model_copy(
        update={
            "strategy": "Hybrid",
            "fallback_count": metrics.fallback_count,
        }
    )
    return result


def main():
    loader = DatasetLoader()
    dataset = loader.load("responses.csv")

    print("=== OLLAMA ===")

    for model_name in MODELS:
        result = run_ollama_benchmark(
            model_name,
            dataset,
        )

        print(result)
        print()

    print(DIV_LINE)
    print(DIV_LINE)
    print()
    print("=== HYBRID ===")

    for model_name in MODELS:
        result = run_hybrid_benchmark(
            model_name,
            dataset,
        )

        print(result)
        print()


if __name__ == "__main__":
    main()
