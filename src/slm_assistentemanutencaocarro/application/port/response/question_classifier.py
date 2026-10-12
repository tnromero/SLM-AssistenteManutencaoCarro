from abc import ABC, abstractmethod

from slm_assistentemanutencaocarro.application.model.response.question_classification import (
    QuestionClassification,
)


class QuestionClassifier(ABC):
    @abstractmethod
    def classify(
        self,
        question: str,
    ) -> QuestionClassification:
        pass
