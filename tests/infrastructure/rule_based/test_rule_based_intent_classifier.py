import pytest

from slm_assistentemanutencaocarro.domain.intent import Intent
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_intent_classifier import (
    RuleBasedIntentClassifier,
)


@pytest.fixture
def classifier():
    return RuleBasedIntentClassifier()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Quando devo trocar o óleo?", Intent.MANUTENCAO),
        ("Quando devo trocar o filtro de ar?", Intent.MANUTENCAO),
        ("Meu carro está fazendo um barulho estranho", Intent.PROBLEMA),
        ("O motor está tremendo", Intent.PROBLEMA),
        ("Quanto custa trocar o óleo?", Intent.CUSTO),
        ("Quanto custa uma revisão?", Intent.CUSTO),
        ("Qual a calibragem dos pneus?", Intent.ESPECIFICACAO),
        ("Quando devo fazer a próxima revisão?", Intent.REVISAO),
        ("Olá", Intent.OUTRO),
    ],
)
def test_should_classify_intent(classifier, text, expected):
    result = classifier.classify(text)

    assert result.intent == expected
