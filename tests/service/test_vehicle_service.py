from slm_assistentemanutencaocarro.repository.vehicle_repository import (
    VehicleRepository,
)
from slm_assistentemanutencaocarro.service.vehicle_service import (
    VehicleService,
)


def create_vehicle_service() -> VehicleService:
    repository:VehicleRepository = VehicleRepository(
        "data/vehicle.json"
    )

    return VehicleService(repository)


def test_should_return_engine_oil():
    vehicle_service = create_vehicle_service()

    assert vehicle_service.get_engine_oil() == "5W-30"


def test_should_return_tire_size():
    vehicle_service = create_vehicle_service()

    assert vehicle_service.get_tire_size() == "205/55 R17"


def test_should_return_tire_pressure():
    vehicle_service = create_vehicle_service()

    assert vehicle_service.get_tire_pressure() == (33.0, 33.0)
