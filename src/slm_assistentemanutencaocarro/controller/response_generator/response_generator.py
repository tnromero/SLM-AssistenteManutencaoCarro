from abc import ABC, abstractmethod

from slm_assistentemanutencaocarro.model.vehicle_answer import VehicleAnswer


class ResponseGenerator(ABC):

    @abstractmethod
    def generate(
        self,
        answer: VehicleAnswer,
    ) -> str:
        pass