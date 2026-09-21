import enum


class QuestionType(enum.StrEnum):
    OLEO_MOTOR = "Óleo do motor"
    PRESSAO_PNEUS = "Pressão dos pneus"
    MEDIDA_PNEUS = "Medida dos pneus"
    DESCONHECIDO = "Desconhecido"
