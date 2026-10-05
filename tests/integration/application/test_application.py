from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.composition import (
    build_application,
)


def test_should_answer_using_selected_vehicle():
    application = build_application(json_file_vehicle="data/vehicle.json")

    application.vehicle_context.select(
        VehicleId(value="t-cross-2022")
    )

    first_result = application.assistant.answer(
        "Qual óleo devo usar?"
    )

    application.vehicle_context.select(
        VehicleId(value="polo-2023")
    )

    second_result = application.assistant.answer(
        "Qual óleo devo usar?"
    )

    assert first_result != second_result
