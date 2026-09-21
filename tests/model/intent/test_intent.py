import pytest
from pydantic import ValidationError

from slm_assistentemanutencaocarro.model.intent.intent import Intent
from slm_assistentemanutencaocarro.model.intent.intent_classification import (
    IntentClassification,
)


def test_should_create_valid_intent_classification():
    result = IntentClassification(intent=Intent.MANUTENCAO)

    assert result.intent == Intent.MANUTENCAO


def test_should_accept_string_value():
    result = IntentClassification(intent="Problema")

    assert result.intent == Intent.PROBLEMA


def test_should_reject_invalid_intent():
    with pytest.raises(ValidationError):
        IntentClassification(intent="Categoria inexistente")
