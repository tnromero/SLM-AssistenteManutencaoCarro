from unittest.mock import Mock

import pytest

from slm_assistentemanutencaocarro.application.model.vehicle_answer import (
    VehicleAnswer,
)
from slm_assistentemanutencaocarro.application.port.response_generator import (
    ResponseGenerator,
)
from slm_assistentemanutencaocarro.application.service.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (
    HybridResponseGenerator,
)


@pytest.fixture
def vehicle_answer() -> VehicleAnswer:
    return VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )


def create_generator(
    slm_response: str = "O óleo recomendado é 5W-40.",
    fallback_response: str = "O óleo especificado é 5W-40.",
    is_valid: bool = True,
):
    slm_generator = Mock(spec=ResponseGenerator)
    fallback_generator = Mock(spec=ResponseGenerator)
    response_validator = Mock(spec=ResponseValidationService)

    slm_generator.generate.return_value = slm_response
    fallback_generator.generate.return_value = fallback_response
    response_validator.validate.return_value = is_valid

    generator = HybridResponseGenerator(
        response_generator=slm_generator,
        fallback_generator=fallback_generator,
        response_validator=response_validator,
    )

    return (
        generator,
        slm_generator,
        fallback_generator,
        response_validator,
    )


def test_should_use_slm_response_when_response_is_valid(vehicle_answer):
    generator, slm_generator, fallback_generator, response_validator = (
        create_generator(
            slm_response="O óleo recomendado é 5W-40.",
            is_valid=True,
        )
    )

    result = generator.generate(vehicle_answer)

    assert result == "O óleo recomendado é 5W-40."

    slm_generator.generate.assert_called_once_with(vehicle_answer)

    response_validator.validate.assert_called_once_with(
        vehicle_answer,
        "O óleo recomendado é 5W-40.",
    )

    fallback_generator.generate.assert_not_called()


def test_should_fallback_when_slm_response_is_invalid(vehicle_answer):
    generator, slm_generator, fallback_generator, response_validator = (
        create_generator(
            slm_response="O óleo recomendado é 0W-20.",
            fallback_response="O óleo especificado é 5W-40.",
            is_valid=False,
        )
    )

    result = generator.generate(vehicle_answer)

    assert result == "O óleo especificado é 5W-40."

    slm_generator.generate.assert_called_once_with(vehicle_answer)

    response_validator.validate.assert_called_once_with(
        vehicle_answer,
        "O óleo recomendado é 0W-20.",
    )

    fallback_generator.generate.assert_called_once_with(vehicle_answer)


def test_should_fallback_when_slm_fails(vehicle_answer):
    generator, slm_generator, fallback_generator, response_validator = (
        create_generator()
    )

    slm_generator.generate.side_effect = RuntimeError(
        "Ollama indisponível"
    )

    result = generator.generate(vehicle_answer)

    assert result == "O óleo especificado é 5W-40."

    slm_generator.generate.assert_called_once_with(vehicle_answer)
    fallback_generator.generate.assert_called_once_with(vehicle_answer)

    response_validator.validate.assert_not_called()


def test_should_count_fallback_when_response_is_invalid(vehicle_answer):
    generator, _, _, _ = create_generator(
        slm_response="O óleo recomendado é 0W-20.",
        is_valid=False,
    )

    generator.generate(vehicle_answer)

    metrics = generator.get_metrics()

    assert metrics.total == 1
    assert metrics.fallback_count == 1
    assert metrics.slm_count == 0
    assert metrics.fallback_rate == 100.0


def test_should_not_count_valid_response_as_fallback(vehicle_answer):
    generator, _, _, _ = create_generator(
        slm_response="O óleo recomendado é 5W-40.",
        is_valid=True,
    )

    generator.generate(vehicle_answer)

    metrics = generator.get_metrics()

    assert metrics.total == 1
    assert metrics.fallback_count == 0
    assert metrics.slm_count == 1
    assert metrics.fallback_rate == 0.0


def test_should_count_fallback_when_slm_fails(vehicle_answer):
    generator, slm_generator, _, _ = create_generator()

    slm_generator.generate.side_effect = RuntimeError(
        "Ollama indisponível"
    )

    generator.generate(vehicle_answer)

    metrics = generator.get_metrics()

    assert metrics.total == 1
    assert metrics.fallback_count == 1
    assert metrics.slm_count == 0
    assert metrics.fallback_rate == 100.0


def test_should_accumulate_fallback_metrics(vehicle_answer):
    generator, _, _, response_validator = create_generator()

    response_validator.validate.side_effect = [
        True,
        True,
        False,
        True,
        False,
        True,
        True,
        False,
        True,
        True,
    ]

    for _ in range(10):
        generator.generate(vehicle_answer)

    metrics = generator.get_metrics()

    assert metrics.total == 10
    assert metrics.slm_count == 7
    assert metrics.fallback_count == 3
    assert metrics.fallback_rate == pytest.approx(30.0)