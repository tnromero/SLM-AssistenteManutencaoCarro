
from slm_assistentemanutencaocarro.application.ports.intent_classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.domain.intent import (
    Intent,
)
from slm_assistentemanutencaocarro.domain.intent_classification import (
    IntentClassification,
)


class HybridIntentClassifier(IntentClassifier):
    def __init__(
        self,
        rule_based_classifier: IntentClassifier,
        ollama_classifier: IntentClassifier,
    ):
        self.rule_based_intent_classifier = rule_based_classifier
        self.ollama_intent_classifier = ollama_classifier

    def classify(self, text: str) -> IntentClassification:

        rule_result: IntentClassification = self.rule_based_intent_classifier.classify(text)

        if rule_result.intent == Intent.OUTRO:
            return self.ollama_intent_classifier.classify(text)
        else:
            return rule_result
