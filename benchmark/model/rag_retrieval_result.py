from dataclasses import dataclass


@dataclass(frozen=True)
class RagRetrievalCaseResult:
    case_id: str
    expected_document_ids: tuple[str, ...]
    retrieved_document_ids: tuple[str, ...]
    hit: bool
    recall: float
    elapsed: float


@dataclass(frozen=True)
class RagRetrievalResult:
    top_k: int
    cases: tuple[RagRetrievalCaseResult, ...]

    @property
    def hit_rate(self) -> float:
        if not self.cases:
            return 0.0

        return sum(case.hit for case in self.cases) / len(self.cases)

    @property
    def mean_recall(self) -> float:
        if not self.cases:
            return 0.0

        return sum(case.recall for case in self.cases) / len(self.cases)

    @property
    def average_time(self) -> float:
        if not self.cases:
            return 0.0

        return sum(case.elapsed for case in self.cases) / len(self.cases)

    def __str__(self) -> str:
        return (
            f"Casos respondíveis: {len(self.cases)}\n"
            f"Hit@{self.top_k}: {self.hit_rate:.2%}\n"
            f"Recall@{self.top_k} médio: {self.mean_recall:.2%}\n"
            f"Tempo médio de recuperação: {self.average_time:.3f}s"
        )
