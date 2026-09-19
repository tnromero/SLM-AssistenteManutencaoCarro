from enum import Enum


class Intent(str, Enum):
    MANUTENCAO = "Manutenção"
    PROBLEMA = "Problema"
    CUSTO = "Custo"
    ESPECIFICACAO = "Especificação"
    REVISAO = "Revisão"
    OUTRO = "Outro"
