from slm_assistentemanutencaocarro.application.services.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


def test_should_accept_non_empty_response():
    service = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-30.",
    )

    assert service.validate(
        answer,
        "Para seu veículo, o óleo especificado é 5W-30.",
    )


def test_should_reject_empty_response():
    service = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-30.",
    )

    assert not service.validate(answer, "")