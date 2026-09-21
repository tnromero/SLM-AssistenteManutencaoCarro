import pytest

from slm_assistentemanutencaocarro.config.settings import Settings
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (
    OllamaResponseGenerator,
)

model_name = Settings().ollama_response_model


@pytest.mark.integration
def test_should_generate_response():

    generator = OllamaResponseGenerator(model=model_name)

    answer = VehicleAnswer(
        question="Qual óleo usar?",
        answer="O óleo especificado é 5W-30.",
    )

    result = generator.generate(answer)

    assert result
    assert isinstance(result, str)
