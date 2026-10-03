from slm_assistentemanutencaocarro.application.ports.vehicle_reader import VehicleReader
from slm_assistentemanutencaocarro.domain.tire_pressure import TirePressure
from slm_assistentemanutencaocarro.domain.vehicle import Vehicle
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class VehicleService:
    
    def __init__(self, 
                 vehicle_reader: VehicleReader, 
                 vehicle_id: VehicleId,
                 ):
        self.vehicle_reader = vehicle_reader
        self.vehicle_id = vehicle_id

    def get_engine_oil(self) -> str | None:
        vehicle = self.vehicle_reader.get_vehicle(
            self.vehicle_id
        )
        return vehicle.engine_oil

    def get_tire_size(self) -> str | None:
        vehicle = self.vehicle_reader.get_vehicle(
            self.vehicle_id
        )
        return vehicle.tire_size

    def get_tire_pressure(self) -> TirePressure | None:
        vehicle = self.vehicle_reader.get_vehicle(
            self.vehicle_id
        )
        return vehicle.tire_pressure

