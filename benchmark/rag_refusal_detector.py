import re
import unicodedata


class RagRefusalDetector:
    @staticmethod
    def detect(response: str) -> bool:
        text = unicodedata.normalize("NFKC", response).strip().casefold()

        # Desconsidera citações para identificar a recusa.
        text = re.sub(r"\[\d+\]", "", text).strip()

        return text.startswith(
            "não encontrei informações suficientes nos documentos disponíveis"
        )
