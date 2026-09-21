from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (
    OllamaResponseGenerator,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


def test_should_generate_response():

    generator = OllamaResponseGenerator()

    answer = VehicleAnswer(
        question="Qual óleo usar?",
        answer="O óleo especificado é 5W-30.",
    )

    result = generator.generate(answer)

    assert result
    assert isinstance(result, str)