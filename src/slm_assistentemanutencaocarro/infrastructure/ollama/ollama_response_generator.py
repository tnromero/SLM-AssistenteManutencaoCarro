import ollama

from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


SYSTEM_PROMPT = """
Você é um assistente de manutenção automotiva.

Você deve apenas transformar a informação fornecida em uma resposta natural.

Regras:
- Não altere valores.
- Não invente informações.
- Não adicione recomendações.
- Não adicione especificações que não estejam no texto fornecido.
- Preserve números, unidades, códigos e medidas exatamente.
- Responda em português.
"""

class OllamaResponseGenerator(ResponseGenerator):
    def __init__(
        self,
        model: str,
    ):
        self.slm_model = model

    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:

        response = ollama.chat(
            model=self.slm_model,
            think=False,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": answer.answer,
                },
            ],
        )

        return response.message.content.strip()
