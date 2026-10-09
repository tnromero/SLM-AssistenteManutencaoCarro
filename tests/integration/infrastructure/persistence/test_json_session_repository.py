from pathlib import Path

import pytest

from slm_assistentemanutencaocarro.application.exception import (
    SessionPersistenceError,
)
from slm_assistentemanutencaocarro.application.model.conversation_message import (  # noqa: E501
    ConversationMessage,
    MessageRole,
)
from slm_assistentemanutencaocarro.application.model.conversation_session import (  # noqa: E501
    ConversationSession,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.persistence.json_session_repository import (  # noqa: E501
    JsonSessionRepository,
)


def test_returns_none_when_file_does_not_exist(tmp_path):
    repository = JsonSessionRepository(tmp_path / "session.json")

    assert repository.load() is None


def test_saves_and_restores_session(tmp_path):
    path = tmp_path / "sessions" / "session.json"

    session = ConversationSession(
        vehicle_id=VehicleId(value="t-cross-2022"),
        messages=(
            ConversationMessage(
                role=MessageRole.USER,
                content="Qual óleo devo usar?",
            ),
            ConversationMessage(
                role=MessageRole.ASSISTANT,
                content="Utilize óleo 5W-40.",
            ),
        ),
    )

    JsonSessionRepository(path).save(session)

    # Uma nova instância simula a leitura após reiniciar.
    restored = JsonSessionRepository(path).load()

    assert restored == session


def test_saves_and_restores_empty_session(tmp_path):
    repository = JsonSessionRepository(tmp_path / "session.json")
    session = ConversationSession(
        vehicle_id=None,
        messages=(),
    )

    repository.save(session)

    assert repository.load() == session


@pytest.mark.parametrize(
    "content",
    [
        "JSON inválido",
        "{}",
        '{"vehicle_id": null, "messages": "inválido"}',
        (
            '{"vehicle_id": null, "messages": '
            '[{"role": "unknown", "content": "Olá"}]}'
        ),
    ],
)
def test_rejects_invalid_file(tmp_path, content):
    path = tmp_path / "session.json"
    path.write_text(content, encoding="utf-8")

    repository = JsonSessionRepository(path)

    with pytest.raises(SessionPersistenceError):
        repository.load()


def test_wraps_write_failure(tmp_path):
    # Um diretório não pode ser usado como arquivo de sessão.
    repository = JsonSessionRepository(tmp_path)
    session = ConversationSession(vehicle_id=None, messages=())

    with pytest.raises(SessionPersistenceError):
        repository.save(session)

def test_failed_replacement_preserves_previous_file(tmp_path, monkeypatch):
    path = tmp_path / "session.json"
    repository = JsonSessionRepository(path)

    previous_session = ConversationSession(
        vehicle_id=VehicleId(value="t-cross-2022"),
        messages=(),
    )
    repository.save(previous_session)
    previous_bytes = path.read_bytes()

    def fail_replace(self, target):
        raise OSError("Falha ao substituir arquivo")

    monkeypatch.setattr(Path, "replace", fail_replace)

    with pytest.raises(SessionPersistenceError):
        repository.save(
            ConversationSession(vehicle_id=None, messages=())
        )

    assert path.read_bytes() == previous_bytes
    assert repository.load() == previous_session
    assert list(tmp_path.glob("*.tmp")) == []