import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_resolver import (
    OllamaQuestionResolver,
)

MODULE = (
    "slm_assistentemanutencaocarro.infrastructure.ollama."
    "ollama_question_resolver"
)


def make_response(content: str):
    return SimpleNamespace(
        message=SimpleNamespace(content=content),
    )


def test_resolves_contextual_question():
    context = ConversationContext()
    context.add_turn(
        "Qual a pressão dos pneus?",
        "A pressão dianteira e traseira está nos dados do veículo.",
    )

    with patch(f"{MODULE}.ollama.chat") as chat:
        chat.return_value = make_response(
            '{"question": "Qual a pressão dos pneus traseiros?"}'
        )

        resolved = OllamaQuestionResolver("qwen3:1.7b").resolve(
            "E nos traseiros?",
            context.get_messages(),
        )

    assert resolved == "Qual a pressão dos pneus traseiros?"


def test_skips_ollama_without_history():
    with patch(f"{MODULE}.ollama.chat") as chat:
        resolved = OllamaQuestionResolver("qwen3:1.7b").resolve(
            "Qual óleo devo usar?",
            (),
        )

    assert resolved == "Qual óleo devo usar?"
    chat.assert_not_called()


def test_preserves_question_when_resolution_is_ambiguous():
    context = ConversationContext()
    context.add_turn("Olá", "Olá!")

    with patch(f"{MODULE}.ollama.chat") as chat:
        chat.return_value = make_response('{"question": null}')

        resolved = OllamaQuestionResolver("qwen3:1.7b").resolve(
            "E ele?",
            context.get_messages(),
        )

    assert resolved == "E ele?"


def test_limits_history_sent_to_ollama():
    context = ConversationContext()
    context.add_turn("Pergunta antiga", "Resposta antiga")
    context.add_turn("Qual a pressão dos pneus?", "Resposta recente")

    with patch(f"{MODULE}.ollama.chat") as chat:
        chat.return_value = make_response('{"question": null}')

        OllamaQuestionResolver("qwen3:1.7b", max_turns=1).resolve(
            "E atrás?",
            context.get_messages(),
        )

        payload = json.loads(
            chat.call_args.kwargs["messages"][1]["content"]
        )

    assert [message["content"] for message in payload["history"]] == [
        "Qual a pressão dos pneus?",
        "Resposta recente",
    ]


def test_propagates_invalid_output():
    context = ConversationContext()
    context.add_turn("Qual óleo?", "5W-40")

    with patch(f"{MODULE}.ollama.chat") as chat:
        chat.return_value = make_response("resposta fora do JSON")

        with pytest.raises(ValidationError):
            OllamaQuestionResolver("qwen3:1.7b").resolve(
                "Qual era mesmo?",
                context.get_messages(),
            )
