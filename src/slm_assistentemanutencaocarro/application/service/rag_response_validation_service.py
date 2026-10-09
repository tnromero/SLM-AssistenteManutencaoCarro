import re

from slm_assistentemanutencaocarro.application.model.rag_context import (
    RagContext,
)


class RagResponseValidationService:
    INSUFFICIENT_INFORMATION_MESSAGE = (
        "Não encontrei informações suficientes nos documentos disponíveis."
    )

    def validate(
        self,
        context: RagContext,
        response: str,
    ) -> bool:
        content = response.strip()

        if not content:
            return False

        if content == self.INSUFFICIENT_INFORMATION_MESSAGE:
            return True

        citation_ids = [
            int(value)
            for value in re.findall(r"\[([0-9]+)\]", content)
        ]

        if not citation_ids:
            return False

        return all(
            1 <= citation_id <= len(context.results)
            for citation_id in citation_ids
        )
