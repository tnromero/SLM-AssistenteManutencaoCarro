import time

from slm_assistentemanutencaocarro.config.model_name import HYBRID, OLLAMA_MODEL, RULE_BASED
from slm_assistentemanutencaocarro.controller.intent_classifier.intent_classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.controller.intent_classifier.ollama_intent_classifier import (
    OllamaIntentClassifier,
)
from slm_assistentemanutencaocarro.controller.intent_classifier.rule_based_intent_classifier import (
    RuleBasedIntentClassifier,
)
from slm_assistentemanutencaocarro.model.intent.intent import (
    Intent,
)
from slm_assistentemanutencaocarro.model.intent.intent_classification import (
    IntentClassification,
)


class HybridIntentClassifier(IntentClassifier):
    def __init__(self, ollama_model: OllamaIntentClassifier):
        super().__init__(model=HYBRID)
        self.rule_based_intent_classifier = RuleBasedIntentClassifier()
        self.ollama_intent_classifier = ollama_model

    def start_classifier(self) -> bool:
        return self.ollama_intent_classifier.start_classifier()

    def close_classifier(self) -> bool:
        return self.ollama_intent_classifier.close_classifier()

    def classify(self, text: str) -> IntentClassification:

        rule_result: IntentClassification = self.rule_based_intent_classifier.classify(
            text
        )

        if rule_result.intent == Intent.OUTRO:
            return self.ollama_intent_classifier.classify(text)
        else:
            return rule_result
