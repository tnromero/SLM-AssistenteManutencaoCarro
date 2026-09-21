from slm_assistentemanutencaocarro.controller.response_generator.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.model.vehicle_answer import VehicleAnswer


class RuleBasedResponseGenerator(ResponseGenerator):

    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:
        return answer.answer