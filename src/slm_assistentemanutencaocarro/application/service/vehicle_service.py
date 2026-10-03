from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.ports.vehicle_reader import (
    VehicleReader,
)
from slm_assistentemanutencaocarro.domain.exception import (
    VehicleNotSelectedError,
)
from slm_assistentemanutencaocarro.domain.tire_pressure import TirePressure
from slm_assistentemanutencaocarro.domain.vehicle import Vehicle


class VehicleService:
    def __init__(
        self,
        vehicle_reader: VehicleReader,
        vehicle_context: VehicleContext,
    ):
        self.vehicle_reader = vehicle_reader
        self.vehicle_context = vehicle_context

    def get_engine_oil(self) -> str | None:
        return self._get_vehicle().engine_oil

    def get_tire_size(self) -> str | None:
        return self._get_vehicle().tire_size

    def get_tire_pressure(self) -> TirePressure | None:
        return self._get_vehicle().tire_pressure

    def _get_vehicle(self) -> Vehicle:
        vehicle_id = self.vehicle_context.get_selected()

        if vehicle_id is None:
            raise VehicleNotSelectedError()

        return self.vehicle_reader.get_vehicle(vehicle_id)