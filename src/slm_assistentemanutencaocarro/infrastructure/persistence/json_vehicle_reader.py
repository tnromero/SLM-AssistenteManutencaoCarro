import json
from pathlib import Path

from slm_assistentemanutencaocarro.application.ports.vehicle_reader import VehicleReader
from slm_assistentemanutencaocarro.domain.vehicle import Vehicle


class JsonVehicleReader(VehicleReader):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> Vehicle:
        with self.file_path.open(encoding="utf-8") as file:
            data = json.load(file)

        return Vehicle.model_validate(data)
