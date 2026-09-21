from pydantic import BaseModel


class IntentClassifierBenchmarkResult(BaseModel):
    model: str
    correct: int
    total: int
    elapsed: float

    @property
    def average_time(self) -> float:
        return self.elapsed / self.total

    @property
    def accuracy(self) -> float:
        return self.correct / self.total * 100

    def display(self, lang: str = "PT") -> None:
        print(f"=== {self.model} ===")
        if lang == "PT":
            self.__display_pt()
        else:
            self.__display_en()

    def __display_pt(self):
        print(f"Modelo: {self.model}")
        print("----------------------------------------")
        print(f"Acurácia: {self.accuracy:.2f}%")
        print(f"Acertos: {self.correct}/{self.total}")
        print(f"Tempo total: {self.elapsed:.2f}s")
        print(f"Tempo médio: {self.average_time:.3f}s")

    def __display_en(self):
        print(f"Model: {self.model}")
        print("----------------------------------------")
        print(f"Accuracy: {self.accuracy:.2f}%")
        print(f"Corrects: {self.correct}/{self.total}")
        print(f"Elapsed: {self.elapsed:.2f}s")
        print(f"Average Time: {self.average_time:.3f}s")
