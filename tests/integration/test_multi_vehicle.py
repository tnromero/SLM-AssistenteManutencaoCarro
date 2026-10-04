from slm_assistentemanutencaocarro.application.context.vehicle_context import VehicleContext
from slm_assistentemanutencaocarro.application.service.vehicle_service import VehicleService
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)


def test_should_switch_selected_vehicle():
    context = VehicleContext()
    reader = JsonVehicleReader("data/vehicle.json")

    service = VehicleService(
        vehicle_reader=reader,
        vehicle_context=context,
    )

    context.select(
        VehicleId(value="t-cross-2022")
    )

    first_oil = service.get_engine_oil()

    context.select(
        VehicleId(value="polo-2023")
    )

    second_oil = service.get_engine_oil()

    assert first_oil != second_oil