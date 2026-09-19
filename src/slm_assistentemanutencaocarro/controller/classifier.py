from abc import ABC, abstractmethod

from slm_assistentemanutencaocarro.model.intent_classification import (
    IntentClassification,
)


class IntentClassifier(ABC):

    @abstractmethod
    def classify(self, text: str) -> IntentClassification:
        pass