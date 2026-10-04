from slm_assistentemanutencaocarro.application.port.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.application.model.vehicle_answer import VehicleAnswer


class RuleBasedResponseGenerator(ResponseGenerator):
    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:
        return answer.answer
