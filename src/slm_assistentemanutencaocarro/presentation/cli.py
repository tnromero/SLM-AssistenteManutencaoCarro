from slm_assistentemanutencaocarro.application.application import Application
from slm_assistentemanutencaocarro.application.context.vehicle_context import VehicleContext
from slm_assistentemanutencaocarro.application.service.assistant_service import AssistantService
from slm_assistentemanutencaocarro.domain.exception import VehicleNotFoundError
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


def run(application: Application) -> None:

    print("Assistente de Manutenção")
    print("Comandos:")
    print(
        "/sair  -> sair do chat"
        "/exit  -> sair do chat"
        "/quit  -> sair do chat"
    )
    print(
        "/vehicles -> listar veiculos conhecidos"
    )

    print(
        "/vehicle <id> -> selecionar um vehicle"
    )

    while True:
        user_input = input("> ").strip()

        if user_input.lower() in {"/sair", "/exit", "/quit"}:
            print("Até mais!")
            break

        if user_input == "/vehicles":
            vehicles = application.vehicle_reader.list_vehicles()
            print("\nVeículos disponíveis:")

            for vehicle in vehicles:
                print(
                    f"- {vehicle.id.value}: "
                    f"{vehicle.brand} {vehicle.model} {vehicle.year}"
                )

            print()
            continue

        if user_input.startswith("/vehicle "):
            vehicle_id_value = user_input.removeprefix(
                "/vehicle "
            ).strip()

            vehicle_id = VehicleId(
                value=vehicle_id_value
            )

            try:
                application.vehicle_reader.get_vehicle(
                    vehicle_id
                )
            except VehicleNotFoundError:
                print("Veículo não encontrado.")
                print()
                continue

            application.vehicle_context.select(
                vehicle_id
            )

            print(
                f"Veículo selecionado: {vehicle_id.value}"
            )
            print()
            continue

        try:
            response = application.assistant.answer(user_input)
            print(response)
        except Exception as exc:
            print(f"Erro ao processar pergunta: {exc}")

        print()