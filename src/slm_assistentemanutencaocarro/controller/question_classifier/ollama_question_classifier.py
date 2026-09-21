import ollama
from pydantic import ValidationError

from slm_assistentemanutencaocarro.config.model_name import OLLAMA_MODEL
from slm_assistentemanutencaocarro.controller.question_classifier.question_classifier import (
    QuestionClassifier,
)
from slm_assistentemanutencaocarro.model.question.question_classification import (
    QuestionClassification,
)


class OllamaQuestionClassifier(QuestionClassifier):

    def __init__(
        self,
        model: str = OLLAMA_MODEL.QWEN_3,
        max_retries: int = 2,
    ):
        self.model = model
        self.max_retries = max_retries

    def classify(
        self,
        question: str,
    ) -> QuestionClassification:

        system_prompt = """
Você é um classificador de perguntas sobre manutenção de veículos.

Classifique a pergunta em exatamente uma das categorias:

- Óleo do motor
- Pressão dos pneus
- Medida dos pneus
- Desconhecido

Regras:

Óleo do motor:
Perguntas sobre óleo, lubrificante, viscosidade ou especificação
do óleo do motor.

Pressão dos pneus:
Perguntas sobre pressão, calibragem ou PSI dos pneus.

Medida dos pneus:
Perguntas sobre tamanho, medida, dimensão ou especificação
dos pneus.

Desconhecido:
Perguntas que não pertencem a nenhuma das categorias acima.

Retorne exclusivamente um JSON compatível com o schema informado.
"""

        last_error = None

        for _ in range(self.max_retries + 1):
            try:
                response = ollama.chat(
                    model=self.model,
                    think=False,
                    options={
                        "temperature": self.config.temperature,
                    },
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": question,
                        },
                    ],
                    format=QuestionClassification.model_json_schema(),
                )

                return QuestionClassification.model_validate_json(
                    response.message.content
                )

            except (ValidationError, ValueError) as exc:
                last_error = exc

            except Exception as exc:
                last_error = exc

        raise RuntimeError(
            f"Falha ao classificar pergunta após "
            f"{self.max_retries + 1} tentativas"
        ) from last_error