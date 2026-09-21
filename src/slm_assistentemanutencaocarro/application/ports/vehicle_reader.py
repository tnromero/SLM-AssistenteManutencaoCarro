from typing import Protocol

from slm_assistentemanutencaocarro.domain.vehicle import Vehicle


class VehicleReader(Protocol):
    def load(self) -> Vehicle: ...
