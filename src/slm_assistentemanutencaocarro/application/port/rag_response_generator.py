from typing import Protocol

from slm_assistentemanutencaocarro.application.model.rag_context import (
    RagContext,
)


class RagResponseGenerator(Protocol):
    def generate(self, context: RagContext) -> str:
        ...
