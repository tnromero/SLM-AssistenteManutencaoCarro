from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class VehicleContext:
    def __init__(self):
        self._vehicle_id: VehicleId | None = None

    def select(self, vehicle_id: VehicleId) -> None:
        self._vehicle_id = vehicle_id

    def get_selected(self) -> VehicleId | None:
        return self._vehicle_id

    def clear(self) -> None:
        self._vehicle_id = None