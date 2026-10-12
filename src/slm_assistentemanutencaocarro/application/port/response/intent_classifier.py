from abc import ABC, abstractmethod

from slm_assistentemanutencaocarro.application.model.response.intent_classification import (
    IntentClassification,
)


class IntentClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> IntentClassification:
        pass
