from typing import Protocol

from slm_assistentemanutencaocarro.application.model.knowledge_chunk import (
    KnowledgeChunk,
)
from slm_assistentemanutencaocarro.application.model.knowledge_document import (
    KnowledgeDocument,
)


class DocumentChunker(Protocol):
    def split(
        self,
        document: KnowledgeDocument,
    ) -> list[KnowledgeChunk]:
        ...
