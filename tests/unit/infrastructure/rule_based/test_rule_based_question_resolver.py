import pytest

from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_resolver import (
    RuleBasedQuestionResolver,
)


@pytest.mark.parametrize(
    "question",
    ["Pode repetir?", "Repita.", "Qual é mesmo?"],
)
def test_resolves_repeat_request(question):
    context = ConversationContext()
    context.add_turn("Qual óleo devo usar?", "5W-40")

    resolved = RuleBasedQuestionResolver().resolve(
        question,
        context.get_messages(),
    )

    assert resolved == "Qual óleo devo usar?"


def test_preserves_independent_question():
    context = ConversationContext()
    context.add_turn("Qual óleo devo usar?", "5W-40")

    resolved = RuleBasedQuestionResolver().resolve(
        "Qual a pressão dos pneus?",
        context.get_messages(),
    )

    assert resolved == "Qual a pressão dos pneus?"


def test_preserves_question_without_history():
    resolved = RuleBasedQuestionResolver().resolve(
        "Pode repetir?",
        (),
    )

    assert resolved == "Pode repetir?"


def test_skips_previous_repeat_requests():
    context = ConversationContext()
    context.add_turn("Qual óleo devo usar?", "5W-40")
    context.add_turn("Pode repetir?", "5W-40")

    resolved = RuleBasedQuestionResolver().resolve(
        "Repita.",
        context.get_messages(),
    )

    assert resolved == "Qual óleo devo usar?"
