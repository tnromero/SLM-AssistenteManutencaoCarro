import pytest

from slm_assistentemanutencaocarro.domain.exception import VehicleNotFoundError
from slm_assistentemanutencaocarro.domain.tire_pressure import TirePressure
from slm_assistentemanutencaocarro.domain.vehicle import Vehicle
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)


def test_should_return_vehicle_by_id():
    reader = JsonVehicleReader("data/vehicle.json")

    creta_id = VehicleId(value="creta-2022")
    creta = Vehicle(
        id = creta_id,
        brand = "Hyundai",
        model = "Creta",
        year = 2022,
        engine = "1.0 TGDI",
        engine_oil = "0W-20",
        tire_pressure=TirePressure(
            front=33, rear=33
        ),
        tire_size="215/60 R17"
    )


    result_vehicle = reader.get_vehicle(vehicle_id=creta_id)

    assert result_vehicle.id == creta.id
    assert result_vehicle.brand == creta.brand
    assert result_vehicle.model == creta.model
    assert result_vehicle.year == creta.year
    assert result_vehicle.engine == creta.engine
    assert result_vehicle.engine_oil == creta.engine_oil
    assert result_vehicle.tire_pressure == creta.tire_pressure
    assert result_vehicle.tire_size == creta.tire_size

def test_should_raise_when_vehicle_id_does_not_exist():
    
    reader = JsonVehicleReader("data/vehicle.json")
    
    creta_id = VehicleId(value="creta-2021")

    with pytest.raises(VehicleNotFoundError):
        reader.get_vehicle(creta_id)