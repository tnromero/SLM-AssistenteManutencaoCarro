from unittest.mock import Mock, patch

import pytest

from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (
    OllamaResponseGenerator,
)



def test_should_generate_response():

    response = Mock()
    response.message.content.strip = "Texto"

    with patch(
        "slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator.ollama.chat",
        return_value=response,
    ) as chat:
        generator = OllamaResponseGenerator(model="qwen3:1.7b")
    
    answer = Mock(spec=VehicleAnswer)
    answer.question = "Qual óleo usar?"
    answer.answer = "O óleo especificado é 5W-30."

    result = generator.generate(answer)

    assert result == "O óleo especificado é 5W-30."
    assert isinstance(result, str)
