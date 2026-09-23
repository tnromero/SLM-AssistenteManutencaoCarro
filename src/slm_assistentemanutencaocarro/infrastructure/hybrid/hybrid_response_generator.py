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
        validator: ResponseValidationService,
        use_slm:bool = False
    ):
        self.rule_generator = rule_generator
        self.ollama_generator = ollama_generator
        self.validator = validator
        self.use_slm = use_slm

    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:
        if self.use_slm:
            try:
                response = self.ollama_generator.generate(answer)

                if self.validator.validate(answer, response):
                    return response
            except Exception:
                pass        
        
        return self.rule_generator.generate(answer)
