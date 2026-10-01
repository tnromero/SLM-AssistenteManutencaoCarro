from abc import ABC, abstractmethod

from benchmark.model.benchmark_result import BenchmarkResult


class BenchmarkInterface(ABC):
    @staticmethod
    @abstractmethod
    def evaluate() -> BenchmarkResult:
        pass
