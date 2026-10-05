from slm_assistentemanutencaocarro.application.model.fallback_metrics import (
    FallbackMetrics,
)
from slm_assistentemanutencaocarro.application.model.vehicle_answer import (
    VehicleAnswer,
)
from slm_assistentemanutencaocarro.application.port.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.application.service.response_validation_service import (
    ResponseValidationService,
)


class HybridResponseGenerator(ResponseGenerator):
    def __init__(
        self,
        response_generator: ResponseGenerator,
        fallback_generator: ResponseGenerator,
        response_validator: ResponseValidationService,
    ):
        self.response_generator = response_generator
        self.fallback_generator = fallback_generator
        self.response_validator = response_validator
        self.metrics = FallbackMetrics()

    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:

        self.metrics.total += 1

        try:
            response = self.response_generator.generate(answer)
        except Exception:
            self.metrics.fallback_count += 1
            return self.fallback_generator.generate(answer)

        is_valid = self.response_validator.validate(
            answer,
            response,
        )

        if is_valid:
            return response

        self.metrics.fallback_count += 1

        return self.fallback_generator.generate(answer)

    def get_metrics(self) -> FallbackMetrics:
        return self.metrics.model_copy()