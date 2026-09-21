from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)


def test_should_load_vehicle_from_json():
    reader = JsonVehicleReader("data/vehicle.json")

    vehicle = reader.load()

    assert vehicle.brand == "Volkswagen"
    assert vehicle.model == "T-Cross"
    assert vehicle.year == 2022
    assert vehicle.engine == "1.0 TSI"
