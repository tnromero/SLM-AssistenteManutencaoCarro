from slm_assistentemanutencaocarro.application.model.vehicle.list_vehicles import (
    ListVehiclesRequest,
    ListVehiclesResult,
)
from slm_assistentemanutencaocarro.application.model.vehicle.vehicle_summary import (
    VehicleSummary,
)
from slm_assistentemanutencaocarro.application.port.vehicle.vehicle_reader import (
    VehicleReader,
)


class ListVehiclesService:
    def __init__(self, vehicle_reader: VehicleReader):
        self.vehicle_reader = vehicle_reader

    def execute(
        self,
        request: ListVehiclesRequest,
    ) -> ListVehiclesResult:
        return ListVehiclesResult(
            vehicles=tuple(
                VehicleSummary(
                    id=vehicle.id.value,
                    brand=vehicle.brand,
                    model=vehicle.model,
                    year=vehicle.year,
                    engine=vehicle.engine,
                )
                for vehicle in self.vehicle_reader.list_vehicles()
            )
        )
