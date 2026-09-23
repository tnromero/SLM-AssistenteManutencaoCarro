from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class ResponseValidationService:
    def validate(
        self,
        answer: VehicleAnswer,
        response: str,
    ) -> bool:
        return bool(response.strip())