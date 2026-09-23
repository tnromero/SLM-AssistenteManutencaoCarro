from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class HybridResponseGenerator(ResponseGenerator):
    def __init__(
        self,
        rule_generator: ResponseGenerator,
        ollama_generator: ResponseGenerator,
        use_slm:bool = False
    ):
        self.rule_generator = rule_generator
        self.ollama_generator = ollama_generator
        self.use_slm = use_slm

    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:
        if self.use_slm:
            try:
                return self.ollama_generator.generate(answer)
            except Exception:
                ...        
        
        return self.rule_generator.generate(answer)
