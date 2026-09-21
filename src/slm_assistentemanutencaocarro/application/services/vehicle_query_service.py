from slm_assistentemanutencaocarro.application.services.vehicle_service import (
    VehicleService,
)
from slm_assistentemanutencaocarro.domain.question_type import QuestionType
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class VehicleQueryService:
    def __init__(
        self,
        vehicle_service: VehicleService,
    ):
        self.vehicle_service = vehicle_service

    def answer(
        self,
        question: str,
        question_type: QuestionType,
    ) -> VehicleAnswer:

        if question_type == QuestionType.OLEO_MOTOR:
            return VehicleAnswer(
                question=question,
                answer=(f"O óleo especificado é {self.vehicle_service.get_engine_oil()}."),
            )

        if question_type == QuestionType.PRESSAO_PNEUS:
            front, rear = self.vehicle_service.get_tire_pressure()

            return VehicleAnswer(
                question=question,
                answer=(
                    f"A pressão configurada é "
                    f"{front:.0f} PSI nos pneus dianteiros "
                    f"e {rear:.0f} PSI nos traseiros."
                ),
            )

        if question_type == QuestionType.MEDIDA_PNEUS:
            return VehicleAnswer(
                question=question,
                answer=(f"A medida dos pneus é {self.vehicle_service.get_tire_size()}."),
            )

        return VehicleAnswer(
            question=question,
            answer=("Ainda não tenho informação suficiente para responder essa pergunta."),
        )
