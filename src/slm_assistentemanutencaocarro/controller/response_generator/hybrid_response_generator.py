from slm_assistentemanutencaocarro.controller.response_generator.ollama_response_generator import (
    OllamaResponseGenerator,
)
from slm_assistentemanutencaocarro.controller.response_generator.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.controller.response_generator.rule_based_response_generator import (
    RuleBasedResponseGenerator,
)
from slm_assistentemanutencaocarro.model.vehicle_answer import VehicleAnswer


class HybridResponseGenerator(ResponseGenerator):

    def __init__(
        self,
        rule_generator: ResponseGenerator,
        ollama_generator: ResponseGenerator,
    ):
        self.rule_generator = (
            rule_generator
        )

        self.ollama_generator = (
            ollama_generator
        )

    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:

        return self.rule_generator.generate(answer)