import json
from contextlib import suppress
from pathlib import Path
from tempfile import NamedTemporaryFile

from pydantic import BaseModel, ConfigDict, ValidationError

from slm_assistentemanutencaocarro.application.exception import (
    SessionPersistenceError,
)
from slm_assistentemanutencaocarro.application.model.conversation_message import (
    ConversationMessage,
    MessageRole,
)
from slm_assistentemanutencaocarro.application.model.conversation_session import (
    ConversationSession,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class StoredMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: MessageRole
    content: str


class StoredSession(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vehicle_id: str | None
    messages: list[StoredMessage]


class JsonSessionRepository:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(self, session: ConversationSession) -> None:
        try:
            stored_session = StoredSession(
                vehicle_id=(
                    session.vehicle_id.value
                    if session.vehicle_id is not None
                    else None
                ),
                messages=[
                    StoredMessage(
                        role=message.role,
                        content=message.content,
                    )
                    for message in session.messages
                ],
            )

            self._write_file(stored_session.model_dump_json(indent=2))
            
        except (OSError, ValidationError) as exc:
            raise SessionPersistenceError(
                "Não foi possível salvar a sessão."
            ) from exc

    def load(self) -> ConversationSession | None:
        try:
            content = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        except (OSError, UnicodeError) as exc:
            raise SessionPersistenceError(
                "Não foi possível ler a sessão."
            ) from exc

        try:
            stored_session = StoredSession.model_validate(json.loads(content))

            return ConversationSession(
                vehicle_id=(
                    VehicleId(value=stored_session.vehicle_id)
                    if stored_session.vehicle_id is not None
                    else None
                ),
                messages=tuple(
                    ConversationMessage(
                        role=message.role,
                        content=message.content,
                    )
                    for message in stored_session.messages
                ),
            )
        except (ValueError, ValidationError) as exc:
            raise SessionPersistenceError(
                "O arquivo de sessão é inválido."
            ) from exc

    def _write_file(self, content: str) -> None:
        temporary_path: Path | None = None

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)

            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                temporary_file.write(content)

            temporary_path.replace(self.path)
        finally:
            if temporary_path is not None:
                with suppress(OSError):
                    temporary_path.unlink(missing_ok=True)