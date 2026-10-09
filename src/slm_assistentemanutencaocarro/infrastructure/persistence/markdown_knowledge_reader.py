from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from slm_assistentemanutencaocarro.application.exception import (
    KnowledgeReadError,
)
from slm_assistentemanutencaocarro.application.model.knowledge_document import (
    KnowledgeDocument,
)
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class ManifestEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    file: str = Field(min_length=1)
    source: str = Field(min_length=1)
    vehicle_id: str | None = None


class KnowledgeManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    documents: list[ManifestEntry]


class MarkdownKnowledgeReader:
    def __init__(self, manifest_path: str | Path):
        self.manifest_path = Path(manifest_path)

    def list_documents(self) -> list[KnowledgeDocument]:
        try:
            manifest = KnowledgeManifest.model_validate_json(
                self.manifest_path.read_text(encoding="utf-8")
            )

            documents = []
            known_ids: set[str] = set()
            base_directory = self.manifest_path.parent.resolve()

            for entry in manifest.documents:
                if entry.id in known_ids:
                    raise ValueError(
                        f"Identidade de documento duplicada: {entry.id}"
                    )

                known_ids.add(entry.id)

                document_path = (
                    base_directory / entry.file
                ).resolve()

                if not document_path.is_relative_to(base_directory):
                    raise ValueError(
                        f"Arquivo fora do diretório de conhecimento: {entry.file}"
                    )

                if document_path.suffix.lower() != ".md":
                    raise ValueError(
                        f"O documento deve ser Markdown: {entry.file}"
                    )

                content = document_path.read_text(encoding="utf-8")

                if not content.strip():
                    raise ValueError(
                        f"Documento vazio: {entry.id}"
                    )

                documents.append(
                    KnowledgeDocument(
                        id=entry.id,
                        title=entry.title,
                        content=content,
                        source=entry.source,
                        vehicle_id=(
                            VehicleId(value=entry.vehicle_id)
                            if entry.vehicle_id is not None
                            else None
                        ),
                    )
                )

            return documents

        except (OSError, ValueError) as exc:
            raise KnowledgeReadError(
                f"Não foi possível carregar a base de conhecimento: {exc}"
            ) from exc
