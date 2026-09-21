import enum


class Intent(enum.StrEnum):
    MANUTENCAO = "Manutenção"
    PROBLEMA = "Problema"
    CUSTO = "Custo"
    ESPECIFICACAO = "Especificação"
    REVISAO = "Revisão"
    OUTRO = "Outro"
