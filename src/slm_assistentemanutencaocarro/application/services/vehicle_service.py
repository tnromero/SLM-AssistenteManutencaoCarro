from slm_assistentemanutencaocarro.application.ports.vehicle_reader import VehicleReader
from slm_assistentemanutencaocarro.domain.vehicle import Vehicle


class VehicleService:
    def __init__(self, reader: VehicleReader):
        self.vehicle = reader.load()

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
