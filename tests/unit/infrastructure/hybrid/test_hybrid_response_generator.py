from unittest.mock import Mock

from slm_assistentemanutencaocarro.application.ports.response_generator import ResponseGenerator
from slm_assistentemanutencaocarro.application.services.response_validation_service import (
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (
    HybridResponseGenerator,
)


def create_generator(rule_response, ollama_response):
    rule_generator = Mock()
    ollama_generator = Mock()
    validator = ResponseValidationService()

    rule_generator.generate.return_value = rule_response
    ollama_generator.generate.return_value = ollama_response

    return (
        HybridResponseGenerator(
            rule_generator=rule_generator,
            ollama_generator=ollama_generator,
            validator=validator,
        ),
        rule_generator,
        ollama_generator,
    )


def test_should_fallback_to_rule_generator_when_slm_fails():
    rule_generator = Mock(spec=ResponseGenerator)
    ollama_generator = Mock(spec=ResponseGenerator)
    validator = Mock(spec=ResponseValidationService)

    answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    rule_generator.generate.return_value = "O óleo especificado é 5W-40."
    ollama_generator.generate.side_effect = RuntimeError("Ollama indisponível")

    generator = HybridResponseGenerator(
        rule_generator=rule_generator,
        ollama_generator=ollama_generator,
        validator=validator,
    )

    result = generator.generate(answer)

    assert result == "O óleo especificado é 5W-40."
    ollama_generator.generate.assert_called_once_with(answer)
    rule_generator.generate.assert_called_once_with(answer)

def test_should_fallback_when_response_is_invalid():
    rule_generator = Mock(spec=ResponseGenerator)
    ollama_generator = Mock(spec=ResponseGenerator)
    validator = Mock(spec=ResponseValidationService)

    answer = VehicleAnswer(
        question="Qual óleo devo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    ollama_generator.generate.return_value = "Resposta inventada."
    validator.validate.return_value = False
    rule_generator.generate.return_value = "O óleo especificado é 5W-40."

    generator = HybridResponseGenerator(
        rule_generator=rule_generator, ollama_generator=ollama_generator, validator=validator
    )

    result = generator.generate(answer)

    assert result == "O óleo especificado é 5W-40."
    validator.validate.assert_called_once_with(
        answer,
        "Resposta inventada.",
    )
    rule_generator.generate.assert_called_once_with(answer)

def test_should_use_ollama_when_response_is_valid():

    hybrid_generator, rule_generator, ollama_generator = create_generator(
        "O óleo especificado é 5W-40.",
        "O óleo recomendado para o veículo é 5W-40.",
    )

    answer = VehicleAnswer(
        question="Qual óleo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    result = hybrid_generator.generate(answer)

    assert result == "O óleo recomendado para o veículo é 5W-40."

    ollama_generator.generate.assert_called_once_with(answer)
    rule_generator.generate.assert_not_called()


def test_should_use_rule_based_when_response_is_invalid():

    hybrid_generator, rule_generator, ollama_generator = create_generator(
        "O óleo especificado é 5W-40.",
        "O óleo recomendado para o veículo é 0W-20.",
    )

    answer = VehicleAnswer(
        question="Qual óleo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    result = hybrid_generator.generate(answer)

    assert result == "O óleo especificado é 5W-40."

    ollama_generator.generate.assert_called_once_with(answer)
    rule_generator.generate.assert_called_once_with(answer)

def test_should_count_fallback():

    generator, rule_generator, ollama_generator = create_generator(
        "O óleo especificado é 5W-40.",
        "O óleo recomendado é 0W-20.",
    )

    answer = VehicleAnswer(
        question="Qual óleo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    generator.generate(answer)

    assert generator.fallback_count == 1

def test_should_not_count_valid_response_as_fallback():

    generator, rule_generator, ollama_generator = create_generator(
        "O óleo especificado é 5W-40.",
        "O óleo recomendado é 5W-40.",
    )

    answer = VehicleAnswer(
        question="Qual óleo usar?",
        answer="O óleo especificado é 5W-40.",
    )

    generator.generate(answer)

    assert generator.fallback_count == 0