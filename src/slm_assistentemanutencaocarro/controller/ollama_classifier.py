import ollama
from pydantic import ValidationError

from slm_assistentemanutencaocarro.controller.classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.model.intent_classification import (
    IntentClassification,
)

SYSTEM_PROMPT = """
Você é um classificador de intenções para um assistente de manutenção de carros.

Classifique a mensagem do usuário em exatamente uma das seguintes intenções:

- Manutenção: perguntas sobre troca de óleo, filtros, manutenção preventiva e itens de manutenção.
- Problema: sintomas, falhas, barulhos, vibrações ou comportamentos anormais do carro.
- Custo: perguntas sobre preço, valor ou quanto será gasto.
- Especificação: informações técnicas do carro, como óleo utilizado, calibragem, pneus e especificações.
- Revisão: perguntas sobre periodicidade ou próxima revisão do veículo.
- Outro: mensagens que não se encaixam nas categorias acima.

Retorne somente o JSON correspondente ao modelo solicitado.
""".strip()


class OllamaIntentClassifier(IntentClassifier):

    def __init__(
        self,
        model: str = "qwen3:1.7b",
    ):
        self.model = model

    def classify(self, text: str) -> IntentClassification:
        try:
            response = ollama.chat(
                model=self.model,
                think=False,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
                format=IntentClassification.model_json_schema(),
            )

            content = response.message.content
            if not isinstance(content, str):
                raise TypeError("A resposta do modelo não contém JSON válido.")

            return IntentClassification.model_validate_json(content)

        except (ValidationError, TypeError, ValueError) as exc:
            raise RuntimeError(
                "O modelo retornou uma classificação inválida."
            ) from exc

        except Exception as exc:
            raise RuntimeError(
                "Falha ao executar classificação com Ollama."
            ) from exc