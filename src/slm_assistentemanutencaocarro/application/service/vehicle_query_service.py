from slm_assistentemanutencaocarro.application.service.vehicle_service import (
    VehicleService,
)
from slm_assistentemanutencaocarro.domain.exception import (
    VehicleDataNotFoundError,
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
            engine_oil = self.vehicle_service.get_engine_oil()

            if engine_oil is None:
                raise VehicleDataNotFoundError(
                    "Informação não encontrada sobre: o óleo motor"
                )

            return VehicleAnswer(
                question=question,
                answer=f"O óleo especificado é {engine_oil}.",
            )

        if question_type == QuestionType.PRESSAO_PNEUS:
            tire_pressure = self.vehicle_service.get_tire_pressure()

            if tire_pressure is None:
                raise VehicleDataNotFoundError(
                    "Informação não encontrada sobre: pressão dos pneus"
                )

            

            return VehicleAnswer(
                question=question,
                answer=(
                    f"A pressão configurada é "
                    f"{tire_pressure.front:.0f} PSI nos pneus dianteiros "
                    f"e {tire_pressure.rear:.0f} PSI nos traseiros."
                ),
            )

        if question_type == QuestionType.MEDIDA_PNEUS:
            tire_size = self.vehicle_service.get_tire_size()

            if tire_size is None:
                raise VehicleDataNotFoundError(
                    "Informação não encontrada sobre: medida dos pneus"
                )

            return VehicleAnswer(
                question=question,
                answer=f"A medida dos pneus é {tire_size}.",
            )

        raise VehicleDataNotFoundError(
            f"Tipo de questão não suportada: {question_type}"
        )
