from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.exception import (
    SessionPersistenceError,
)
from slm_assistentemanutencaocarro.application.model.conversation_session import (
    ConversationSession,
)
from slm_assistentemanutencaocarro.application.port.session_repository import (
    SessionRepository,
)
from slm_assistentemanutencaocarro.application.port.vehicle_reader import (
    VehicleReader,
)
from slm_assistentemanutencaocarro.domain.exception import (
    VehicleNotFoundError,
)


class SessionService:
    def __init__(
        self,
        repository: SessionRepository,
        vehicle_reader: VehicleReader,
        vehicle_context: VehicleContext,
        conversation_context: ConversationContext,
    ):
        self.repository = repository
        self.vehicle_reader = vehicle_reader
        self.vehicle_context = vehicle_context
        self.conversation_context = conversation_context

    def save(self) -> None:
        session = ConversationSession(
            vehicle_id=self.vehicle_context.get_selected(),
            messages=self.conversation_context.get_messages(),
        )

        self.repository.save(session)

    def restore(self) -> bool:
        session = self.repository.load()

        if session is None:
            return False

        try:
            if session.vehicle_id is not None:
                self.vehicle_reader.get_vehicle(session.vehicle_id)

            self.conversation_context.restore(session.messages)
        except (VehicleNotFoundError, ValueError) as exc:
            raise SessionPersistenceError(
                "A sessão contém veículo inexistente ou histórico inválido."
            ) from exc

        if session.vehicle_id is None:
            self.vehicle_context.clear()
        else:
            self.vehicle_context.select(session.vehicle_id)

        return True