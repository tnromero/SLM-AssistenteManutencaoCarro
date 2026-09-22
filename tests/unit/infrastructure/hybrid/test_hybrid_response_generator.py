from unittest.mock import Mock

from slm_assistentemanutencaocarro.application.ports.response_generator import ResponseGenerator
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (
    HybridResponseGenerator,
)


def test_should_preserve_rule_based_response():
    rule_generator = Mock(spec=ResponseGenerator)
    ollama_generator = Mock(spec=ResponseGenerator)

    answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-30.",
    )

    rule_generator.generate.return_value = "O óleo especificado é 5W-30."

    generator = HybridResponseGenerator(
        rule_generator=rule_generator,
        ollama_generator=ollama_generator,
    )

    result = generator.generate(answer)

    assert result == "O óleo especificado é 5W-30."
    ollama_generator.generate.assert_not_called()
