from slm_assistentemanutencaocarro.application.model.vehicle_answer import (
    VehicleAnswer,
)
from slm_assistentemanutencaocarro.application.port.response_generator import (
    ResponseGenerator,
)


class RuleBasedResponseGenerator(ResponseGenerator):
    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:
        return answer.answer
