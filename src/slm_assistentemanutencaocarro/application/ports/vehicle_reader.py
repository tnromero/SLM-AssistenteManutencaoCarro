from abc import abstractmethod
from typing import Protocol

from slm_assistentemanutencaocarro.domain.vehicle import Vehicle
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class VehicleReader(Protocol):
    @abstractmethod
    def get_vehicle(
        self,
        vehicle_id: VehicleId,
    ) -> Vehicle:
        pass
