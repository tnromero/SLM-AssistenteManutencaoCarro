from dataclasses import dataclass

from slm_assistentemanutencaocarro.application.model.conversation_message import (
    ConversationMessage,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


@dataclass(frozen=True)
class ConversationSession:
    vehicle_id: VehicleId | None
    messages: tuple[ConversationMessage, ...]
