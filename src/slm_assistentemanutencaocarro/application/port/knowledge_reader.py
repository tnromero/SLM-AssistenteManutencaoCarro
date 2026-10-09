from typing import Protocol

from slm_assistentemanutencaocarro.application.model.knowledge_document import (
    KnowledgeDocument,
)


class KnowledgeReader(Protocol):
    def list_documents(self) -> list[KnowledgeDocument]:
        ...
