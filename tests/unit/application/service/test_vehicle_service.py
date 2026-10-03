from slm_assistentemanutencaocarro.application.context.vehicle_context import VehicleContext
from slm_assistentemanutencaocarro.application.ports.vehicle_reader import VehicleReader
from slm_assistentemanutencaocarro.application.service.vehicle_service import (
    VehicleService,
)
from slm_assistentemanutencaocarro.domain.tire_pressure import TirePressure
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)

reader = JsonVehicleReader("data/vehicle.json")

def test_should_return_engine_oil_from_selected_vehicle():

    vehicle_context = VehicleContext()
    vehicle_context.select(VehicleId(
            value="t-cross-2022"
        ))
    vehicle_service = VehicleService(
        vehicle_reader=reader,
        vehicle_context=vehicle_context
    )

    assert vehicle_service.get_engine_oil() == "5W-40"

    vehicle_context.select(VehicleId(
                value="polo-2023"
            ))
    vehicle_service = VehicleService(
        vehicle_reader=reader,
        vehicle_context=vehicle_context
    )

    assert vehicle_service.get_engine_oil() == "0W-20"


def test_should_return_tire_size_from_selected_vehicle():

    vehicle_context = VehicleContext()
    vehicle_context.select(VehicleId(
            value="t-cross-2022"
        ))
    vehicle_service = VehicleService(
        vehicle_reader=reader,
        vehicle_context=vehicle_context
    )

    assert vehicle_service.get_tire_size() == "205/55 R16"


def test_should_return_tire_pressure():
    vehicle_context = VehicleContext()
    vehicle_context.select(VehicleId(
            value="t-cross-2022"
        ))
    vehicle_service = VehicleService(
        vehicle_reader=reader,
        vehicle_context=vehicle_context
    )

    assert vehicle_service.get_tire_pressure() == TirePressure(front=32, rear=32)
