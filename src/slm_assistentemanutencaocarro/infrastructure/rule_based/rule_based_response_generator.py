from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class RuleBasedResponseGenerator(ResponseGenerator):
    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:
        return answer.answer
