import ollama
from pydantic import ValidationError

from slm_assistentemanutencaocarro.controller.intent_classifier import (
    IntentClassifier,
)
from slm_assistentemanutencaocarro.model.intent_classification import (
    IntentClassification,
)

FEW_SHOT_EXAMPLES = """
Exemplos:

"Quando devo trocar o óleo?" -> Manutenção
"Preciso fazer a troca do óleo do meu carro" -> Manutenção

"Meu carro está fazendo um barulho estranho" -> Problema
"O motor está tremendo" -> Problema

"Quanto custa trocar o óleo?" -> Custo
"Quanto vou pagar na revisão?" -> Custo

"Qual a calibragem dos pneus?" -> Especificação
"Que pressão devo colocar nos pneus?" -> Especificação
"Qual o tamanho do pneu?" -> Especificação

"Quando devo fazer a próxima revisão?" -> Revisão
"De quanto em quanto tempo devo revisar o carro?" -> Revisão

"Olá" -> Outro
"Bom dia" -> Outro
""".strip()

SYSTEM_PROMPT = f"""
Você é um classificador de intenções para um assistente de manutenção de carros.

Classifique a mensagem do usuário em exatamente uma das seguintes intenções:

- Manutenção: perguntas sobre troca de óleo, filtros, manutenção preventiva e itens de manutenção.
- Problema: sintomas, falhas, barulhos, vibrações ou comportamentos anormais do carro.
- Custo: perguntas sobre preço, valor ou quanto será gasto.
- Especificação: informações técnicas do carro, como óleo utilizado, calibragem, pneus e especificações.
- Revisão: perguntas sobre periodicidade ou próxima revisão do veículo.
- Outro: mensagens que não se encaixam nas categorias acima.

{FEW_SHOT_EXAMPLES}

Retorne somente o JSON correspondente ao modelo solicitado.
""".strip()


class OllamaIntentClassifier(IntentClassifier):

    def __init__(self, model: str):
        super().__init__(model)

    def start_classifier(self) -> bool:
        try:
            ollama.chat(
                model=self.get_model_name(),
                think=False,
                messages=[
                    {
                        "role": "user",
                        "content": "Oi",
                    }
                ],
            )
            return True
        except Exception:
            return False

    def close_classifier(self) -> bool:
        try:
            ollama.chat(
                model=self.model,
                think=False,
                messages=[],
                keep_alive=0
            )
            return True
        except Exception:
            return False

    def classify(self, text: str) -> IntentClassification:
        try:
            response = ollama.chat(
                model=self.get_model_name(),
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
            raise RuntimeError("O modelo retornou uma classificação inválida.") from exc

        except Exception as exc:
            raise RuntimeError("Falha ao executar classificação com Ollama.") from exc
