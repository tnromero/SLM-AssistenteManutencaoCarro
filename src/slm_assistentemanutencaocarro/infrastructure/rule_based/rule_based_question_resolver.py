from slm_assistentemanutencaocarro.application.model.conversation_message import (
    ConversationMessage,
    MessageRole,
)


class RuleBasedQuestionResolver:
    REPEAT_REQUESTS = {
        "pode repetir",
        "repita",
        "qual é mesmo",
        "qual era mesmo",
    }

    def resolve(
        self,
        question: str,
        history: tuple[ConversationMessage, ...],
    ) -> str:
        if not self._is_repeat_request(question):
            return question

        for message in reversed(history):
            if (
                message.role == MessageRole.USER
                and not self._is_repeat_request(message.content)
            ):
                return message.content

        return question

    def _is_repeat_request(self, question: str) -> bool:
        normalized = question.strip().casefold().rstrip("?!.")

        return normalized in self.REPEAT_REQUESTS