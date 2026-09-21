from slm_assistentemanutencaocarro.model.intent import Intent
from slm_assistentemanutencaocarro.model.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.repository.vehicle_repository import (
    VehicleRepository,
)
from slm_assistentemanutencaocarro.service.vehicle_query_service import (
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.service.vehicle_service import (
    VehicleService,
)


def create_vehicle_query_service() -> VehicleQueryService:
    repository: VehicleRepository = VehicleRepository("data/vehicle.json")

    vehicle_service: VehicleService = VehicleService(repository)

    return VehicleQueryService(vehicle_service)


def test_should_answer_engine_oil():
    service: VehicleQueryService = create_vehicle_query_service()

    result: VehicleAnswer = service.answer(
        "Qual óleo usar no motor?", Intent.ESPECIFICACAO
    )

    assert result.answer == "O óleo especificado é 5W-30."


def test_should_answer_tire_pressure():
    service = create_vehicle_query_service()

    result = service.answer(
        "Qual a pressão dos pneus?",
        Intent.ESPECIFICACAO,
    )

    assert result.answer == (
        "A pressão configurada é 33 PSI nos pneus dianteiros e 33 PSI nos traseiros."
    )


def test_should_answer_tire_size():
    service = create_vehicle_query_service()

    result = service.answer(
        "Qual o tamanho do pneu?",
        Intent.ESPECIFICACAO,
    )

    assert result.answer == ("A medida dos pneus é 205/55 R17.")


def test_should_not_invent_maintenance_information():
    service = create_vehicle_query_service()

    result = service.answer(
        "Devo trocar o filtro?",
        Intent.MANUTENCAO,
    )

    assert "não tenho conhecimento" not in result.answer.lower()
    assert "manutenção" in result.answer.lower()
