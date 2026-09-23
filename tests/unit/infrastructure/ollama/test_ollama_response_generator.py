from unittest.mock import Mock, patch

from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (
    SYSTEM_PROMPT,
    OllamaResponseGenerator,
)


def test_should_generate_response():

    response = Mock()
    response.message.content = "O óleo especificado é 5W-30."
    
    answer = Mock(spec=VehicleAnswer)
    answer.question = "Qual óleo usar?"
    answer.answer = "O óleo especificado é 5W-30."

    with patch(
        "slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator.ollama.chat",
        return_value=response,
    ) as chat:
        generator = OllamaResponseGenerator(model="qwen3:1.7b")
        result = generator.generate(answer)

    assert result == "O óleo especificado é 5W-30."
    assert isinstance(result, str)
    chat.assert_called_once_with(
        model="qwen3:1.7b",
        think=False,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": "O óleo especificado é 5W-30.",
            },
        ]
    )
