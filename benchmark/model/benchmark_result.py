from pydantic import BaseModel


class BenchmarkResult(BaseModel):
    model: str
    correct: int
    total: int
    elapsed: float
    strategy: str | None = None
    fallback_count: int = 0

    @property
    def average_time(self) -> float:
        if self.total == 0:
            return 0.0

        return self.elapsed / self.total

    @property
    def accuracy(self) -> float:
        if self.total == 0:
            return 0.0
        
        return self.correct / self.total * 100

    @property
    def fallback_rate(self) -> float:

        if self.total == 0:
            return 0.0

        return self.fallback_count / self.total * 100

    def __str__(self) -> str:
        return (
            f"Modelo: {self.model}\n"
            f"  Estratégia : {self.strategy}\n"
            f"  Acertos    : {self.correct}/{self.total}\n"
            f"  Acurácia   : {self.accuracy:.2f}%\n"
            f"  Tempo total: {self.elapsed:.2f}s\n"
            f"  Tempo médio: {self.average_time:.3f}s\n"
            f"  Fallbacks  : {self.fallback_rate:.2f}%\n"
        )