from slm_assistentemanutencaocarro.application.service.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.application.model.vehicle_answer import VehicleAnswer


def test_should_accept_same_oil_viscosity():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    result = validator.validate(
        answer,
        "Para esse veículo, utilize óleo 5W-40.",
    )

    assert result is True


def test_should_reject_different_oil_viscosity():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    result = validator.validate(
        answer,
        "Para esse veículo, utilize óleo 0W-20.",
    )

    assert result is False


def test_should_accept_same_pressure_in_psi():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual a pressão dos pneus?",
        answer="A pressão recomendada é 32 PSI.",
    )

    result = validator.validate(
        answer,
        "Mantenha os pneus calibrados em 32 psi.",
    )

    assert result is True


def test_should_reject_different_pressure_in_psi():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual a pressão dos pneus?",
        answer="A pressão recomendada é 32 PSI.",
    )

    result = validator.validate(
        answer,
        "Mantenha os pneus calibrados em 35 PSI.",
    )

    assert result is False


def test_should_accept_bar_with_comma_or_dot():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual a pressão dos pneus?",
        answer="A pressão recomendada é 2,2 bar.",
    )

    result = validator.validate(
        answer,
        "A pressão correta é 2.2 bar.",
    )

    assert result is True


def test_should_accept_same_tire_size():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual o tamanho do pneu?",
        answer="A medida recomendada é 205/55 R16.",
    )

    result = validator.validate(
        answer,
        "O veículo utiliza pneus 205/55 R16.",
    )

    assert result is True


def test_should_reject_different_tire_size():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual o tamanho do pneu?",
        answer="A medida recomendada é 205/55 R16.",
    )

    result = validator.validate(
        answer,
        "O veículo utiliza pneus 215/55 R16.",
    )

    assert result is False


def test_should_require_all_factual_values():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Quais são as especificações?",
        answer="Utilize óleo 5W-40 e calibre os pneus em 32 PSI.",
    )

    result = validator.validate(
        answer,
        "Utilize óleo 5W-40 e mantenha os pneus em 32 PSI.",
    )

    assert result is True


def test_should_reject_when_one_factual_value_is_missing():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Quais são as especificações?",
        answer="Utilize óleo 5W-40 e calibre os pneus em 32 PSI.",
    )

    result = validator.validate(
        answer,
        "Utilize óleo 5W-40.",
    )

    assert result is False


def test_should_fallback_to_text_validation_when_no_fact_is_found():
    validator = ResponseValidationService()

    answer = VehicleAnswer(
        question="Qual a recomendação?",
        answer="Realize a manutenção preventiva regularmente.",
    )

    result = validator.validate(
        answer,
        "Realize a manutenção preventiva regularmente.",
    )

    assert result is True
