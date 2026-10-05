from slm_assistentemanutencaocarro.application.model.conversation_message import (
    ConversationMessage,
    MessageRole,
)


class ConversationContext:
    def __init__(self, max_turns: int = 5):
        if max_turns < 1:
            raise ValueError("max_turns deve ser maior que zero.")

        self._max_messages = max_turns * 2
        self._messages: list[ConversationMessage] = []

    def add_turn(self, question: str, response: str) -> None:
        self._messages.extend(
            [
                ConversationMessage(
                    role=MessageRole.USER,
                    content=question,
                ),
                ConversationMessage(
                    role=MessageRole.ASSISTANT,
                    content=response,
                ),
            ]
        )

        self._messages = self._messages[-self._max_messages:]

    def get_messages(self) -> tuple[ConversationMessage, ...]:
        return tuple(self._messages)

    def clear(self) -> None:
        self._messages.clear()

    def restore(
        self,
        messages: tuple[ConversationMessage, ...],
    ) -> None:
        if len(messages) % 2 != 0:
            raise ValueError("O histórico deve conter turnos completos.")

        for index in range(0, len(messages), 2):
            if (
                messages[index].role != MessageRole.USER
                or messages[index + 1].role != MessageRole.ASSISTANT
            ):
                raise ValueError(
                    "Cada turno deve conter uma pergunta e uma resposta."
                )

        self._messages = list(messages[-self._max_messages:])
