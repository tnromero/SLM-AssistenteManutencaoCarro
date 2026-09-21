from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class HybridResponseGenerator(ResponseGenerator):
    def __init__(
        self,
        rule_generator: ResponseGenerator,
        ollama_generator: ResponseGenerator,
    ):
        self.rule_generator = rule_generator
        self.ollama_generator = ollama_generator

    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:

        return self.rule_generator.generate(answer)
