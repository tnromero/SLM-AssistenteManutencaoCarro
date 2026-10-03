import csv
from pathlib import Path


class DatasetLoader:
    def load(
        self,
        filename: str,
        enconding: str = "utf=8",
        delimiter: str = ",",
        quotechar: str | None = '"',
        escapechar: str | None = None,
        doublequote: bool = True,
    ) -> list[dict[str, str]]:
        path = Path(__file__).parent / "dataset" / filename

        with path.open(newline="", encoding=enconding) as file:
            return list(
                csv.DictReader(
                    f=file,
                    delimiter=delimiter,
                    quotechar=quotechar,
                    escapechar=escapechar,
                    doublequote=doublequote
                )
            )
