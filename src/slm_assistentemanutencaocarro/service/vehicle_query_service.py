from slm_assistentemanutencaocarro.model.intent import Intent
from slm_assistentemanutencaocarro.model.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.service.vehicle_service import (
    VehicleService,
)


class VehicleQueryService:

    def __init__(self, vehicle_service: VehicleService):
        self.vehicle_service = vehicle_service

    def answer(
        self,
        question: str,
        intent: Intent,
    ) -> VehicleAnswer:

        if intent == Intent.ESPECIFICACAO:
            return self._answer_specification(question)

        if intent == Intent.MANUTENCAO:
            return VehicleAnswer(
                question=question,
                answer=(
                    "Essa pergunta requer uma informação "
                    "de manutenção específica do veículo."
                ),
            )

        return VehicleAnswer(
            question=question,
            answer=(
                "Ainda não tenho conhecimento suficiente "
                "para responder essa pergunta."
            ),
        )

    def _answer_specification(
        self,
        question: str,
    ) -> VehicleAnswer:

        question_lower = question.lower()

        if "óleo" in question_lower or "oleo" in question_lower:
            return VehicleAnswer(
                question=question,
                answer=(
                    f"O óleo especificado é "
                    f"{self.vehicle_service.get_engine_oil()}."
                ),
            )

        if "pneu" in question_lower and (
            "pressão" in question_lower
            or "pressao" in question_lower
            or "calibr" in question_lower
        ):
            front, rear = (
                self.vehicle_service.get_tire_pressure()
            )

            return VehicleAnswer(
                question=question,
                answer=(
                    f"A pressão configurada é "
                    f"{front:.0f} PSI nos pneus dianteiros "
                    f"e {rear:.0f} PSI nos traseiros."
                ),
            )

        if "pneu" in question_lower and (
            "tamanho" in question_lower
            or "medida" in question_lower
        ):
            return VehicleAnswer(
                question=question,
                answer=(
                    f"A medida dos pneus é "
                    f"{self.vehicle_service.get_tire_size()}."
                ),
            )

        return VehicleAnswer(
            question=question,
            answer=(
                "Tenho a intenção identificada como "
                "Especificação, mas ainda não tenho "
                "essa informação cadastrada."
            ),
        )