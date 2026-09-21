from enum import Enum


class QuestionType(str, Enum):
    OLEO_MOTOR = "Óleo do motor"
    PRESSAO_PNEUS = "Pressão dos pneus"
    MEDIDA_PNEUS = "Medida dos pneus"
    DESCONHECIDO = "Desconhecido"