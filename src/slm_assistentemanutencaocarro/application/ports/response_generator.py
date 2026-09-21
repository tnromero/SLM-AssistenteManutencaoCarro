from abc import ABC, abstractmethod

from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class ResponseGenerator(ABC):
    @abstractmethod
    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:
        pass
