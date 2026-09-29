from slm_assistentemanutencaocarro.application.ports.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.application.services.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class HybridResponseGenerator(ResponseGenerator):
    def __init__(
        self,
        rule_generator: ResponseGenerator,
        ollama_generator: ResponseGenerator,
        validator: ResponseValidationService
    ):
        self.rule_generator = rule_generator
        self.ollama_generator = ollama_generator
        self.validator = validator
        self.fallback_count = 0

    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:
        try:
            response = self.ollama_generator.generate(answer)

            if self.validator.validate(answer, response):
                return response
        except Exception:
            pass        

        self.fallback_count += 1
        return self.rule_generator.generate(answer)

    @property
    def fallback_call_count(self) -> int:
        return self.fallback_count
