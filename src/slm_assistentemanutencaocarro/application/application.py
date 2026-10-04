from dataclasses import dataclass

from slm_assistentemanutencaocarro.application.context.vehicle_context import VehicleContext
from slm_assistentemanutencaocarro.application.port.vehicle_reader import VehicleReader
from slm_assistentemanutencaocarro.application.service.assistant_service import AssistantService


@dataclass
class Application:
    assistant: AssistantService
    vehicle_context: VehicleContext
    vehicle_reader: VehicleReader