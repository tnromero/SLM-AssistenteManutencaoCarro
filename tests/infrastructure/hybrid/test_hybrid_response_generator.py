from unittest.mock import Mock

from slm_assistentemanutencaocarro.config.settings import Settings
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (
    HybridResponseGenerator,
)

model_name = Settings().ollama_response_model


def test_should_use_rule_based_generator():

    rule_generator = Mock()
    ollama_generator = Mock()

    rule_generator.generate.return_value = "O óleo especificado é 5W-30."

    generator = HybridResponseGenerator(
        rule_generator=rule_generator,
        ollama_generator=ollama_generator,
    )

    answer = VehicleAnswer(
        question="Qual óleo usar?",
        answer="O óleo especificado é 5W-30.",
    )

    result = generator.generate(answer)

    assert result == "O óleo especificado é 5W-30."

    rule_generator.generate.assert_called_once_with(answer)

    ollama_generator.generate.assert_not_called()
