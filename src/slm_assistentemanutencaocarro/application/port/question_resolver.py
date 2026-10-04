from typing import Protocol

from slm_assistentemanutencaocarro.application.model.conversation_message import (
    ConversationMessage,
)


class QuestionResolver(Protocol):
    def resolve(
        self,
        question: str,
        history: tuple[ConversationMessage, ...],
    ) -> str:
        ...