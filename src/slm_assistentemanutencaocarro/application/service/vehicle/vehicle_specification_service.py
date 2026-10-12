from slm_assistentemanutencaocarro.application.model.vehicle.vehicle_specification import (  # noqa: E501
    VehicleSpecification,
    VehicleSpecificationRequest,
    VehicleSpecificationResult,
)
from slm_assistentemanutencaocarro.application.port.vehicle.vehicle_reader import (  # noqa: E501
    VehicleReader,
)


class VehicleSpecificationService:
    def __init__(self, vehicle_reader: VehicleReader):
        self.vehicle_reader = vehicle_reader

    def execute(
        self,
        request: VehicleSpecificationRequest,
    ) -> VehicleSpecificationResult:
        vehicle = self.vehicle_reader.get_vehicle(request.vehicle_id)

        match request.specification:
            case VehicleSpecification.ENGINE_OIL:
                value = vehicle.engine_oil
            case VehicleSpecification.TIRE_PRESSURE:
                value = vehicle.tire_pressure
            case VehicleSpecification.TIRE_SIZE:
                value = vehicle.tire_size
            case _:
                raise ValueError("Especificação não suportada.")

        return VehicleSpecificationResult(
            vehicle_id=vehicle.id,
            specification=request.specification,
            value=value,
        )
