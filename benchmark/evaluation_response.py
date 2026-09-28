import csv

from benchmark.benchmark_result import (
    BenchmarkResult,
)
from benchmark.response_generator_benchmark import ResponseGeneratorBenchamark
from slm_assistentemanutencaocarro.application.services.response_validation_service import (
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

# Modelos
QWEN_3 = "qwen3:1.7b"
LLAMA_3_2 = "llama3.2:1b"

# Arquivos de testes/treinamentos
csv_files = [
    "benchmark/data/responses.csv",
]


def load_test_cases(
    csv_file_name: str, enconding_file: str = "utf-8", delimiter=","
) -> list[dict[str, str]]:

    test_cases: list[dict[str, str]]
    with open(csv_file_name, encoding=enconding_file) as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        test_cases = list(reader)

    return test_cases


def main():

    for csv_file_name in csv_files:
        test_case = load_test_cases(csv_file_name=csv_file_name)

        result: BenchmarkResult = ResponseGeneratorBenchamark().evaluate(
            "QWEN_3",
            OllamaResponseGenerator(model=QWEN_3),
            test_case,
        )

        result: BenchmarkResult = ResponseGeneratorBenchamark().evaluate(
            "Hibrido",
            HybridResponseGenerator(
                rule_generator=RuleBasedResponseGenerator(),
                ollama_generator=OllamaResponseGenerator(model=QWEN_3),
                validator=ResponseValidationService(),
                use_slm=True
            ),
            test_case,
        )
        result.display("PT")

        print()
        print()
        print("====================================================")


if __name__ == "__main__":
    main()
