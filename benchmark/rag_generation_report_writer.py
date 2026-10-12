import json
from dataclasses import asdict
from pathlib import Path

from benchmark.model.rag_generation_case_result import (
    RagGenerationCaseResult,
)


class RagGenerationReportWriter:
    @staticmethod
    def write(
        path: Path,
        *,
        model: str,
        top_k: int,
        cases: list[RagGenerationCaseResult],
    ) -> None:
        payload = {
            "model": model,
            "top_k": top_k,
            "cases": [
                {
                    **asdict(case),
                    "manual_review": {
                        "verdict": None,
                        "notes": "",
                    },
                }
                for case in cases
            ],
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
