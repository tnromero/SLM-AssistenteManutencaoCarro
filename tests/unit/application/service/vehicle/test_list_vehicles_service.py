from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from slm_assistentemanutencaocarro.application.model.vehicle.list_vehicles import (
    ListVehiclesRequest,
)
from slm_assistentemanutencaocarro.application.port.vehicle.vehicle_reader import (
    VehicleReader,
)
from slm_assistentemanutencaocarro.application.service.vehicle.list_vehicles_service import (
    ListVehiclesService,
)
from slm_assistentemanutencaocarro.domain.vehicle import Vehicle
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


def test_lists_vehicle_identity_without_maintenance_fields():
    reader = Mock(spec=VehicleReader)
    reader.list_vehicles.return_value = [
        Vehicle(
            id=VehicleId(value="t-cross-2022"),
            brand="Volkswagen",
            model="T-Cross",
            year=2022,
            engine="1.0 TSI",
            engine_oil="5W-40",
        )
    ]

    result = ListVehiclesService(reader).execute(ListVehiclesRequest())

    assert result.model_dump(mode="json") == {
        "vehicles": [
            {
                "id": "t-cross-2022",
                "brand": "Volkswagen",
                "model": "T-Cross",
                "year": 2022,
                "engine": "1.0 TSI",
            }
        ]
    }
    reader.get_vehicle.assert_not_called()


def test_returns_empty_list_when_no_vehicles_exist():
    reader = Mock(spec=VehicleReader)
    reader.list_vehicles.return_value = []

    result = ListVehiclesService(reader).execute(ListVehiclesRequest())

    assert result.vehicles == ()


def test_rejects_unexpected_arguments():
    with pytest.raises(ValidationError):
        ListVehiclesRequest.model_validate({"vehicle_id": "t-cross-2022"})
