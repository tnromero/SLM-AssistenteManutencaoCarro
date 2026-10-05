from typing import Protocol

from slm_assistentemanutencaocarro.application.model.conversation_session import (
    ConversationSession,
)


class SessionRepository(Protocol):
    def save(self, session: ConversationSession) -> None:
        ...

    def load(self) -> ConversationSession | None:
        ...
