from slm_assistentemanutencaocarro.application.ports.vehicle_reader import VehicleReader
from slm_assistentemanutencaocarro.application.services.vehicle_service import (
    VehicleService,
)
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)


def create_vehicle_service() -> VehicleService:
    reader: VehicleReader = JsonVehicleReader("data/vehicle.json")

    return VehicleService(reader)


def test_should_return_engine_oil():
    vehicle_service = create_vehicle_service()

    assert vehicle_service.get_engine_oil() == "5W-30"


def test_should_return_tire_size():
    vehicle_service = create_vehicle_service()

    assert vehicle_service.get_tire_size() == "205/55 R17"


def test_should_return_tire_pressure():
    vehicle_service = create_vehicle_service()

    assert vehicle_service.get_tire_pressure() == (33.0, 33.0)
