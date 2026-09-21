from evaluation_questions import evaluate, load_dataset

from slm_assistentemanutencaocarro.controller.question_classifier.hybrid_question_classifier import (
    HybridQuestionClassifier,
)
from slm_assistentemanutencaocarro.controller.question_classifier.ollama_question_classifier import (
    OllamaQuestionClassifier,
)
from slm_assistentemanutencaocarro.controller.question_classifier.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)


def main():
    dataset = load_dataset(
        "data/questions_generalization.csv"
    )

    evaluate(
        RuleBasedQuestionClassifier(),
        dataset,
    )

    evaluate(
        OllamaQuestionClassifier(),
        dataset,
    )

    evaluate(
        HybridQuestionClassifier(RuleBasedQuestionClassifier(), OllamaQuestionClassifier()),
        dataset,
    )


if __name__ == "__main__":
    main()