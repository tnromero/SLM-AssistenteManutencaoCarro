from pathlib import Path

from pydantic import BaseModel, ConfigDict

from benchmark.model.rag_case import RagCase


class RagDataset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cases: list[RagCase]


class RagDatasetLoader:
    def load(self, filename: str = "rag_cases.json") -> list[RagCase]:
        path = Path(__file__).parent / "dataset" / filename

        dataset = RagDataset.model_validate_json(
            path.read_text(encoding="utf-8")
        )

        case_ids = [case.id for case in dataset.cases]

        if len(set(case_ids)) != len(case_ids):
            raise ValueError("Identidades de casos duplicadas.")

        return dataset.cases
