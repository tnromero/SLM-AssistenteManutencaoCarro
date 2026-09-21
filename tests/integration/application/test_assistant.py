import pytest

from slm_assistentemanutencaocarro.infrastructure.composition import (
    create_assistant,
)


@pytest.mark.integration
def test_should_answer_engine_oil_question():
    assistant = create_assistant("data/vehicle.json")

    result = assistant.answer("Qual óleo devo usar?")

    assert result == "O óleo especificado é 5W-30."

@pytest.mark.integration
def test_should_answer_tire_pressure_question():
    assistant = create_assistant("data/vehicle.json")

    result = assistant.answer("Qual a pressão dos pneus?")

    assert "33 PSI" in result

@pytest.mark.integration
def test_should_answer_tire_size_question():
    assistant = create_assistant("data/vehicle.json")

    result = assistant.answer("Qual a medida dos pneus?")

    assert "205/55 R17" in result