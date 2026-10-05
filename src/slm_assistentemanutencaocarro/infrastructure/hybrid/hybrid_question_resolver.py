from slm_assistentemanutencaocarro.application.model.conversation_message import (
    ConversationMessage,
)
from slm_assistentemanutencaocarro.application.port.question_resolver import (
    QuestionResolver,
)


class HybridQuestionResolver(QuestionResolver):
    def __init__(
        self,
        rule_question_resolver: QuestionResolver,
        slm_question_resolver: QuestionResolver,
    ):
        self.rule_question_resolver = rule_question_resolver
        self.slm_question_resolver = slm_question_resolver

    def resolve(
        self,
        question: str,
        history: tuple[ConversationMessage, ...],
    ) -> str:
        if not history:
            return question

        resolved_question = self.rule_question_resolver.resolve(
            question=question,
            history=history,
        )

        if resolved_question != question:
            return resolved_question

        try:
            resolved_question = self.slm_question_resolver.resolve(
                question=question,
                history=history,
            )
            return resolved_question
        except Exception:
            # Adicionar log depois
            return question