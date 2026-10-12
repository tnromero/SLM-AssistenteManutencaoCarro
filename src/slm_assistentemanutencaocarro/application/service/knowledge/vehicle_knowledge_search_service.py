from slm_assistentemanutencaocarro.application.model.knowledge.vehicle_knowledge_search import (  # noqa: E501
    KnowledgePassage,
    VehicleKnowledgeSearchRequest,
    VehicleKnowledgeSearchResult,
)
from slm_assistentemanutencaocarro.application.port.vehicle.vehicle_reader import (  # noqa: E501
    VehicleReader,
)
from slm_assistentemanutencaocarro.application.service.knowledge.knowledge_search_service import (  # noqa: E501
    KnowledgeSearchService,
)


class VehicleKnowledgeSearchService:
    def __init__(
        self,
        vehicle_reader: VehicleReader,
        search_service: KnowledgeSearchService,
    ):
        self.vehicle_reader = vehicle_reader
        self.search_service = search_service

    def execute(
        self,
        request: VehicleKnowledgeSearchRequest,
    ) -> VehicleKnowledgeSearchResult:
        self.vehicle_reader.get_vehicle(request.vehicle_id)

        results = self.search_service.search(
            question=request.question,
            top_k=request.top_k,
            vehicle_id=request.vehicle_id,
        )

        return VehicleKnowledgeSearchResult(
            vehicle_id=request.vehicle_id,
            passages=tuple(
                KnowledgePassage(
                    chunk_id=result.chunk.id,
                    document_id=result.chunk.document_id,
                    title=result.chunk.title,
                    content=result.chunk.content,
                    source=result.chunk.source,
                    score=result.score,
                )
                for result in results
            ),
        )
