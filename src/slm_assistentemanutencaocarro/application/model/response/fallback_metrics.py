from pydantic import BaseModel


class FallbackMetrics(BaseModel):
    total: int = 0
    fallback_count: int = 0

    @property
    def slm_count(self) -> int:
        return self.total - self.fallback_count

    @property
    def fallback_rate(self) -> float:
        if self.total == 0:
            return 0.0

        return self.fallback_count / self.total * 100