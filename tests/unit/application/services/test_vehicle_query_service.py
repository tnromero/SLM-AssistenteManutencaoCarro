from slm_assistentemanutencaocarro.application.services.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.application.services.vehicle_service import VehicleService
from slm_assistentemanutencaocarro.domain.question_type import QuestionType
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (
    JsonVehicleReader,
)


def create_vehicle_query_service() -> VehicleQueryService:
    reader = JsonVehicleReader("data/vehicle.json")

    vehicle_service: VehicleService = VehicleService(reader)

    return VehicleQueryService(vehicle_service)


def test_should_answer_engine_oil():
    service: VehicleQueryService = create_vehicle_query_service()

    result: VehicleAnswer = service.answer("Qual óleo usar no motor?", QuestionType.OLEO_MOTOR)

    assert result.answer == "O óleo especificado é 5W-30."


def test_should_answer_tire_pressure():
    service = create_vehicle_query_service()

    result: VehicleAnswer = service.answer("Qual a pressão dos pneus?", QuestionType.PRESSAO_PNEUS)

    assert result.answer == (
        "A pressão configurada é 33 PSI nos pneus dianteiros e 33 PSI nos traseiros."
    )


def test_should_answer_tire_size():
    service = create_vehicle_query_service()

    result: VehicleAnswer = service.answer("Qual o tamanho do pneu?", QuestionType.MEDIDA_PNEUS)

    assert result.answer == ("A medida dos pneus é 205/55 R17.")


def test_should_not_invent_maintenance_information():
    service = create_vehicle_query_service()

    result: VehicleAnswer = service.answer("Devo trocar o filtro?", QuestionType.DESCONHECIDO)

    assert "não tenho conhecimento" not in result.answer.lower()
