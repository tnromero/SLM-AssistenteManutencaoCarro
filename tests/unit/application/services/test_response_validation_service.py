from slm_assistentemanutencaocarro.application.services.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


def test_should_accept_non_empty_response():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    assert validator.validate(
        answer,
        "Para seu veículo, o óleo especificado é 5W-40.",
    )


def test_should_reject_empty_response():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    assert not validator.validate(answer, "")


def test_should_accept_response_with_same_oil():
    validator = ResponseValidationService()

    answer = VehicleAnswer(question="Qual óleo devo usar?", answer="O óleo especificado é 5W-40.")

    assert validator.validate(
        answer,
        "Para o seu veículo, o óleo especificado é 5W-40.",
    )


def test_should_reject_response_with_different_oil():
    validator = ResponseValidationService()

    answer = VehicleAnswer(question="Qual óleo devo usar?", answer="O óleo especificado é 5W-40.")

    assert not validator.validate(
        answer,
        "Para o seu veículo, o óleo especificado é 0W-20.",
    )


def test_should_accept_response_with_same_tire_pressure():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual a pressão correta dos pneus?", answer="A pressão correta é 33 PSI."
    )

    assert validator.validate(
        answer,
        "A pressão recomendada para os pneus é 33 PSI.",
    )


def test_should_reject_response_with_different_tire_pressure():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual a pressão correta dos pneus?", answer="A pressão correta é 33 PSI."
    )

    assert not validator.validate(
        answer,
        "A pressão recomendada para os pneus é 35 PSI.",
    )

def test_should_accept_same_tire_size():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual o tamanho do pneu?",
        answer="A medida dos pneus é 205/55 R17.",
    )

    assert validator.validate(
        answer,
        "A medida recomendada é 205/55 R17.",
    )


def test_should_reject_different_tire_size():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual o tamanho do pneu?",
        answer="A medida dos pneus é 205/55 R17.",
    )

    assert not validator.validate(
        answer,
        "A medida recomendada é 215/55 R17.",
    )