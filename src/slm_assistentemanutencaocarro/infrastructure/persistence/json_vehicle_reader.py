import json
from pathlib import Path

from slm_assistentemanutencaocarro.application.ports.vehicle_reader import VehicleReader
from slm_assistentemanutencaocarro.domain.exception import VehicleNotFoundError
from slm_assistentemanutencaocarro.domain.vehicle import Vehicle
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class JsonVehicleReader(VehicleReader):
    def __init__(self, json_file: str | Path):
        self.json_file = Path(json_file)

    def get_vehicle(
        self,
        vehicle_id: VehicleId,
    ) -> Vehicle:
        
        with self.json_file.open(encoding="utf-8") as file:
            data = json.load(file)

        vehicle_data = data["vehicles"].get(
            vehicle_id.value
        )

        if vehicle_data is None:
            raise VehicleNotFoundError(
                f"Vehicle not found: {vehicle_id.value}"
            )

        return Vehicle(
            id=vehicle_id,
            **vehicle_data,
        )