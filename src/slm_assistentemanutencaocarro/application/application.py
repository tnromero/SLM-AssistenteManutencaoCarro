from dataclasses import dataclass

from slm_assistentemanutencaocarro.application.context.conversation_context import (
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.port.vehicle_reader import (
    VehicleReader,
)
from slm_assistentemanutencaocarro.application.service.assistant_service import (
    AssistantService,
)
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (
    KnowledgeSearchService,
)
from slm_assistentemanutencaocarro.application.service.knowledge_service import (
    KnowledgeService,
)
from slm_assistentemanutencaocarro.application.service.rag_service import (
    RagService,
)
from slm_assistentemanutencaocarro.application.service.session_service import (
    SessionService,
)


@dataclass
class Application:
    assistant: AssistantService
    vehicle_context: VehicleContext
    vehicle_reader: VehicleReader
    conversation_context: ConversationContext
    session_service: SessionService
    knowledge_service: KnowledgeService
    knowledge_search_service: KnowledgeSearchService
    rag_service: RagService
