import csv
import time

from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_question_classifier import (
    HybridQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_classifier import (
    OllamaQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)
from slm_assistentemanutencaocarro.domain.question_type import QuestionType


def load_dataset(path: str):
    with open(path, encoding="utf-8") as file:
        return list(csv.DictReader(file))


def evaluate(classifier, dataset):
    start = time.perf_counter()

    correct = 0

    for item in dataset:
        result = classifier.classify(item["question"])

        if result.question_type.value == item["expected"]:
            correct += 1
        else:
            print(
                f"ERRO [{classifier.__class__.__name__}]: "
                f"{item['question']} | "
                f"esperado={item['expected']} | "
                f"obtido={result.question_type.value}"
            )

    elapsed = time.perf_counter() - start

    total = len(dataset)

    print(f"\n=== {classifier.__class__.__name__} ===")
    print(f"Acurácia: {correct / total * 100:.2f}%")
    print(f"Acertos: {correct}/{total}")
    print(f"Tempo total: {elapsed:.2f}s")
    print(f"Tempo médio: {elapsed / total:.3f}s")


def main():
    dataset = load_dataset("data/questions.csv")

    evaluate(
        RuleBasedQuestionClassifier(),
        dataset,
    )

    evaluate(
        OllamaQuestionClassifier(),
        dataset,
    )

    evaluate(
        HybridQuestionClassifier(
            RuleBasedQuestionClassifier(), OllamaQuestionClassifier()
        ),
        dataset,
    )


if __name__ == "__main__":
    main()
