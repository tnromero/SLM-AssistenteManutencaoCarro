from benchmark.benchmark.question_classifier_benchmark import (
    QuestionClassifierBenchmark,
)
from benchmark.dataset_loader import DatasetLoader
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_classifier import (
    OllamaQuestionClassifier,
)

QWEN_3 = "qwen3:1.7b"

def main():
    loader = DatasetLoader()

    dataset = loader.load("questions.csv")

    question_classifier = OllamaQuestionClassifier(QWEN_3)

    result = QuestionClassifierBenchmark.evaluate(
        evaluate_name="QWEN_3",
        question_classifier=question_classifier,
        dataset=dataset,
    )

    print(result)


if __name__ == "__main__":
    main()