from slm_assistentemanutencaocarro.repository.vehicle_repository import (
    VehicleRepository,
)


def test_should_load_vehicle_from_json():
    repository = VehicleRepository(
        "data/vehicle.json"
    )

    vehicle = repository.load()

    assert vehicle.brand == "Volkswagen"
    assert vehicle.model == "T-Cross"
    assert vehicle.year == 2022
    assert vehicle.engine == "1.0 TSI"