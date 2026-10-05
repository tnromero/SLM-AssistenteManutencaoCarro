from unittest.mock import Mock

import pytest

from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.port.question_resolver import (
    QuestionResolver,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_question_resolver import (
    HybridQuestionResolver,
)


@pytest.fixture
def resolver_setup():
    context = ConversationContext()
    context.add_turn("Qual óleo devo usar?", "Utilize óleo 5W-40.")

    rule_question_resolver = Mock(spec=QuestionResolver)
    slm_question_resolver = Mock(spec=QuestionResolver)

    question_resolver = HybridQuestionResolver(
        rule_question_resolver=rule_question_resolver,
        slm_question_resolver=slm_question_resolver,
    )

    return question_resolver, context.get_messages(), rule_question_resolver, slm_question_resolver


def test_skips_resolvers_without_history(resolver_setup):
    question_resolver, _, rule_question_resolver, slm_question_resolver = resolver_setup

    assert question_resolver.resolve("Qual óleo devo usar?", ()) == (
        "Qual óleo devo usar?"
    )

    rule_question_resolver.resolve.assert_not_called()
    slm_question_resolver.resolve.assert_not_called()


def test_uses_rule_resolution_without_calling_slm(resolver_setup):
    question_resolver, history, rule_question_resolver, slm_question_resolver = resolver_setup
    rule_question_resolver.resolve.return_value = "Qual óleo devo usar?"

    resolved = question_resolver.resolve("Pode repetir?", history)

    assert resolved == "Qual óleo devo usar?"
    slm_question_resolver.resolve.assert_not_called()


def test_uses_slm_when_rules_preserve_question(resolver_setup):
    question_resolver, history, rule_question_resolver, slm_question_resolver = resolver_setup
    question = "Qual era a viscosidade indicada?"

    rule_question_resolver.resolve.return_value = question
    slm_question_resolver.resolve.return_value = (
        "Qual a viscosidade do óleo indicada para o motor?"
    )

    resolved = question_resolver.resolve(question, history)

    assert resolved == "Qual a viscosidade do óleo indicada para o motor?"
    slm_question_resolver.resolve.assert_called_once_with(
        question=question,
        history=history,
    )


def test_preserves_original_question_when_slm_fails(resolver_setup):
    question_resolver, history, rule_question_resolver, slm_question_resolver = resolver_setup
    question = "Qual era a viscosidade indicada?"

    rule_question_resolver.resolve.return_value = question
    slm_question_resolver.resolve.side_effect = RuntimeError("Ollama indisponível")

    assert question_resolver.resolve(question, history) == question
