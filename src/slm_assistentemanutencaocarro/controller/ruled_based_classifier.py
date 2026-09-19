from slm_assistentemanutencaocarro.controller.classifier import IntentClassifier
from slm_assistentemanutencaocarro.model.intent import Intent
from slm_assistentemanutencaocarro.model.intent_classification import (
    IntentClassification,
)


class RuleBasedIntentClassifier(IntentClassifier):

    def classify(self, text: str) -> IntentClassification:
        text = text.lower()

        if any(
            keyword in text
            for keyword in [
                "barulho",
                "ruído",
                "tremendo",
                "trepidando",
                "falhando",
            ]
        ):
            return IntentClassification(intent=Intent.PROBLEMA)

        if any(
            keyword in text
            for keyword in [
                "quanto custa",
                "preço",
                "valor",
                "custa",
            ]
        ):
            return IntentClassification(intent=Intent.CUSTO)

        if any(
            keyword in text
            for keyword in [
                "revisão",
                "revisao",
                "periodicidade",
            ]
        ):
            return IntentClassification(intent=Intent.REVISAO)

        if any(
            keyword in text
            for keyword in [
                "calibragem",
                "pressão dos pneus",
                "pressao dos pneus",
                "especificação",
                "especificacao",
            ]
        ):
            return IntentClassification(intent=Intent.ESPECIFICACAO)

        if any(
            keyword in text
            for keyword in [
                "trocar o óleo",
                "troca de óleo",
                "troca de oleo",
                "filtro",
                "manutenção",
                "manutencao",
            ]
        ):
            return IntentClassification(intent=Intent.MANUTENCAO)

        return IntentClassification(intent=Intent.OUTRO)