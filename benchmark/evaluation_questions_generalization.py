from evaluation_questions import evaluate, load_dataset

from slm_assistentemanutencaocarro.config.settings import Settings
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_question_classifier import (
    HybridQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_classifier import (
    OllamaQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_classifier import (
    RuleBasedQuestionClassifier,
)

settings = Settings()


def main():
    dataset = load_dataset("benchmark/data/questions_generalization.csv")

    evaluate(
        RuleBasedQuestionClassifier(),
        dataset,
    )

    evaluate(
        OllamaQuestionClassifier(model=settings.ollama_question_model),
        dataset,
    )

    evaluate(
        HybridQuestionClassifier(
            RuleBasedQuestionClassifier(),
            OllamaQuestionClassifier(model=settings.ollama_question_model),
        ),
        dataset,
    )


if __name__ == "__main__":
    main()
