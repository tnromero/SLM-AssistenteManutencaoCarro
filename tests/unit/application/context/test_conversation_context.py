import pytest

from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.model.conversation_message import (
    MessageRole,
)


def test_starts_without_messages():
    context = ConversationContext()

    assert context.get_messages() == ()


def test_adds_question_and_response_in_order():
    context = ConversationContext()

    context.add_turn("Qual óleo?", "5W-40")

    messages = context.get_messages()

    assert len(messages) == 2
    assert messages[0].role == MessageRole.USER
    assert messages[0].content == "Qual óleo?"
    assert messages[1].role == MessageRole.ASSISTANT
    assert messages[1].content == "5W-40"


def test_discards_oldest_complete_turn():
    context = ConversationContext(max_turns=2)

    context.add_turn("Pergunta 1", "Resposta 1")
    context.add_turn("Pergunta 2", "Resposta 2")
    context.add_turn("Pergunta 3", "Resposta 3")

    assert [
        message.content for message in context.get_messages()
    ] == [
        "Pergunta 2",
        "Resposta 2",
        "Pergunta 3",
        "Resposta 3",
    ]


def test_previous_snapshot_is_preserved():
    context = ConversationContext()
    context.add_turn("Pergunta 1", "Resposta 1")

    snapshot = context.get_messages()

    context.add_turn("Pergunta 2", "Resposta 2")

    assert len(snapshot) == 2
    assert len(context.get_messages()) == 4


def test_clears_history():
    context = ConversationContext()
    context.add_turn("Qual óleo?", "5W-40")

    context.clear()

    assert context.get_messages() == ()


@pytest.mark.parametrize("max_turns", [0, -1])
def test_rejects_invalid_limit(max_turns):
    with pytest.raises(ValueError):
        ConversationContext(max_turns=max_turns)