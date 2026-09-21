import ollama

from slm_assistentemanutencaocarro.config.model_name import OLLAMA_MODEL
from slm_assistentemanutencaocarro.controller.response_generator.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.model.vehicle_answer import VehicleAnswer


class OllamaResponseGenerator(ResponseGenerator):

    def __init__(
        self,
        model: str = OLLAMA_MODEL.QWEN_3,
    ):
        self.model = model

    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:

        system_prompt = """
Você é um assistente de manutenção automotiva.

Transforme a informação fornecida pelo sistema
em uma resposta curta, clara e natural.

Regras:
- Não invente informações.
- Não altere valores.
- Não altere especificações.
- Não adicione informações que não estejam na resposta.
- Responda em português.
- Seja objetivo.
"""

        response = ollama.chat(
            model=self.model,
            think=False,
            options={
                "temperature": 0.7,
            },
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": answer.answer,
                },
            ],
        )

        return response.message.content.strip()