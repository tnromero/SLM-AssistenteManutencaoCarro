import json
from pathlib import Path

from slm_assistentemanutencaocarro.application.ports.vehicle_reader import VehicleReader
from slm_assistentemanutencaocarro.domain.exception import VehicleNotFoundError
from slm_assistentemanutencaocarro.domain.vehicle import Vehicle
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


class JsonVehicleReader(VehicleReader):
    
    def __init__(self, json_file: str | Path):
        self.json_file = Path(json_file)
        self._vehicles = self._load()

    def _load(self) -> dict:
        with self.json_file.open(
            encoding="utf-8",
        ) as file:
            return json.load(file)["vehicles"]
    
    def get_vehicle(
        self,
        vehicle_id: VehicleId,
    ) -> Vehicle:
        
        vehicle_data = self._vehicles.get(
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

    def list_vehicles(self) -> list[Vehicle]:
        return [
            Vehicle(
                id=VehicleId(value=vehicle_id),
                **vehicle_data,
            )
            for vehicle_id, vehicle_data in self._vehicles.items()
        ]
