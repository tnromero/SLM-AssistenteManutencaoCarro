from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from slm_assistentemanutencaocarro.application.model.vehicle.vehicle_specification import (  # noqa: E501
    VehicleSpecification,
    VehicleSpecificationRequest,
)
from slm_assistentemanutencaocarro.application.port.vehicle.vehicle_reader import (  # noqa: E501
    VehicleReader,
)
from slm_assistentemanutencaocarro.application.service.vehicle.vehicle_specification_service import (  # noqa: E501
    VehicleSpecificationService,
)
from slm_assistentemanutencaocarro.domain.exception import VehicleNotFoundError
from slm_assistentemanutencaocarro.domain.vehicle import Vehicle
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


@pytest.mark.parametrize(
    ("specification", "expected"),
    [
        (VehicleSpecification.ENGINE_OIL, "5W-40"),
        (VehicleSpecification.TIRE_SIZE, "205/60 R16"),
        (VehicleSpecification.TIRE_PRESSURE, None),
    ],
)
def test_queries_specification_for_requested_vehicle(specification, expected):
    vehicle_id = VehicleId(value="vehicle-test")
    reader = Mock(spec=VehicleReader)
    reader.get_vehicle.return_value = Vehicle(
        id=vehicle_id,
        brand="Marca",
        model="Modelo",
        year=2022,
        engine="1.0",
        engine_oil="5W-40",
        tire_size="205/60 R16",
    )

    result = VehicleSpecificationService(reader).execute(
        VehicleSpecificationRequest(
            vehicle_id=vehicle_id,
            specification=specification,
        )
    )

    assert result.vehicle_id == vehicle_id
    assert result.specification == specification
    assert result.value == expected
    reader.get_vehicle.assert_called_once_with(vehicle_id)


def test_propagates_vehicle_not_found():
    reader = Mock(spec=VehicleReader)
    reader.get_vehicle.side_effect = VehicleNotFoundError("Não encontrado")

    request = VehicleSpecificationRequest(
        vehicle_id=VehicleId(value="missing"),
        specification=VehicleSpecification.ENGINE_OIL,
    )

    with pytest.raises(VehicleNotFoundError):
        VehicleSpecificationService(reader).execute(request)


def test_rejects_unknown_specification():
    with pytest.raises(ValidationError):
        VehicleSpecificationRequest.model_validate(
            {
                "vehicle_id": {"value": "vehicle-test"},
                "specification": "wheel_torque",
            }
        )
