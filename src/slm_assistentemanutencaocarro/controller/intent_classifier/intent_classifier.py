from abc import ABC, abstractmethod

from slm_assistentemanutencaocarro.model.intent.intent_classification import (
    IntentClassification,
)


class IntentClassifier(ABC):
    def __init__(
        self,
        model: str,
    ):
        self.__model = model

    def get_model_name(self) -> str:
        return self.__model

    @abstractmethod
    def classify(self, text: str) -> IntentClassification:
        pass

    @abstractmethod
    def start_classifier(self) -> bool:
        pass

    @abstractmethod
    def close_classifier(self) -> bool:
        pass
