from slm_assistentemanutencaocarro.model.vehicle import Vehicle
from slm_assistentemanutencaocarro.repository.vehicle_repository import (
    VehicleRepository,
)


class VehicleService:

    def __init__(self, repository: VehicleRepository):
        self.vehicle = repository.load()

    def get_vehicle(self) -> Vehicle:
        return self.vehicle

    def get_engine_oil(self) -> str:
        return self.vehicle.engine_oil

    def get_tire_size(self) -> str:
        return self.vehicle.tire_size

    def get_tire_pressure(self) -> tuple[float, float]:
        return (
            self.vehicle.tire_pressure_front,
            self.vehicle.tire_pressure_rear,
        )