import csv
from pathlib import Path


class DatasetLoader:
    def load(self, filename: str, enconding: str = "utf=8") -> list[dict[str, str]]:
        path = Path(__file__).parent / "dataset" / filename

        with path.open(newline="", encoding=enconding) as file:
            return list(csv.DictReader(file))
