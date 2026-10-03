from unittest.mock import Mock

import pytest

from slm_assistentemanutencaocarro.application.service.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.application.service.vehicle_service import VehicleService
from slm_assistentemanutencaocarro.domain.exception import VehicleDataNotFoundError
from slm_assistentemanutencaocarro.domain.question_type import QuestionType
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)


def create_vehicle_query_service() -> VehicleQueryService:
    reader = JsonVehicleReader("data/vehicle.json")

    tcross_id = VehicleId(value="t-cross-2022")
    vehicle_service = VehicleService(reader, tcross_id)

    return VehicleQueryService(vehicle_service)


def test_should_answer_engine_oil():
    service: VehicleQueryService = create_vehicle_query_service()

    result: VehicleAnswer = service.answer("Qual óleo usar no motor?", QuestionType.OLEO_MOTOR)

    assert result.answer == "O óleo especificado é 5W-40."


def test_should_answer_tire_pressure():
    service = create_vehicle_query_service()

    result: VehicleAnswer = service.answer("Qual a pressão dos pneus?", QuestionType.PRESSAO_PNEUS)

    assert result.answer == (
        "A pressão configurada é 32 PSI nos pneus dianteiros e 32 PSI nos traseiros."
    )


def test_should_answer_tire_size():
    service = create_vehicle_query_service()

    result: VehicleAnswer = service.answer("Qual o tamanho do pneu?", QuestionType.MEDIDA_PNEUS)

    assert result.answer == ("A medida dos pneus é 205/55 R16.")

def test_should_raise_when_engine_oil_data_is_missing():
    vehicle_service = Mock(spec=VehicleService)

    vehicle_service.get_engine_oil.return_value = None

    service = VehicleQueryService(vehicle_service)

    with pytest.raises(VehicleDataNotFoundError):
        service.answer(
            "Qual óleo devo usar?",
            QuestionType.OLEO_MOTOR,
        )

def test_should_raise_when_tire_pressure_data_is_missing():
    vehicle_service = Mock(spec=VehicleService)

    vehicle_service.get_tire_pressure.return_value = None

    service = VehicleQueryService(vehicle_service)

    with pytest.raises(VehicleDataNotFoundError):
        service.answer(
            "Qual a pressão dos pneus?", QuestionType.PRESSAO_PNEUS
        )

def test_should_raise_when_tire_size_data_is_missing():
    vehicle_service = Mock(spec=VehicleService)

    vehicle_service.get_tire_size.return_value = None

    service = VehicleQueryService(vehicle_service)

    with pytest.raises(VehicleDataNotFoundError):
        service.answer(
            "Qual a medida dos pneus",
            QuestionType.MEDIDA_PNEUS,
        )
