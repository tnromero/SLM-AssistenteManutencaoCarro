import pytest

from slm_assistentemanutencaocarro.application.context.vehicle_context import VehicleContext
from slm_assistentemanutencaocarro.application.exception import VehicleNotSelectedError
from slm_assistentemanutencaocarro.application.service.vehicle_service import VehicleService
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)


def test_should_raise_when_no_vehicle_is_selected():
    context = VehicleContext()
    reader = JsonVehicleReader("data/vehicle.json")

    service = VehicleService(
        vehicle_reader=reader,
        vehicle_context=context,
    )

    with pytest.raises(VehicleNotSelectedError):
        service.get_engine_oil()