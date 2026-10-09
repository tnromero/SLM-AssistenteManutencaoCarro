from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.model.knowledge_document import (
    KnowledgeDocument,
)
from slm_assistentemanutencaocarro.application.port.knowledge_reader import (
    KnowledgeReader,
)


class KnowledgeService:
    def __init__(
        self,
        knowledge_reader: KnowledgeReader,
        vehicle_context: VehicleContext,
    ):
        self.knowledge_reader = knowledge_reader
        self.vehicle_context = vehicle_context

    def list_documents(self) -> list[KnowledgeDocument]:
        selected_vehicle = self.vehicle_context.get_selected()

        return [
            document
            for document in self.knowledge_reader.list_documents()
            if document.vehicle_id is None
            or document.vehicle_id == selected_vehicle
        ]
