from slm_assistentemanutencaocarro.controller.response_generator.rule_based_response_generator import (
    RuleBasedResponseGenerator,
)
from slm_assistentemanutencaocarro.model.vehicle_answer import VehicleAnswer


def test_should_generate_response():

    generator = RuleBasedResponseGenerator()

    answer = VehicleAnswer(
        question="Qual óleo usar?",
        answer="O óleo especificado é 5W-30.",
    )

    result = generator.generate(answer)

    assert result == "O óleo especificado é 5W-30."