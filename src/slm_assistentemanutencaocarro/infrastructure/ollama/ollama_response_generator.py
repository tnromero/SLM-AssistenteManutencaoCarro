import ollama

from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


SYSTEM_PROMPT = """
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
