from slm_assistentemanutencaocarro.application.application import Application
from slm_assistentemanutencaocarro.domain.exception import VehicleNotFoundError
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


def run(application: Application) -> None:

    print("Assistente de Manutenção")
    print("Comandos:")
    print(
        "/exit         -> sair do chat\n"
        "/quit         -> sair do chat\n"
        "/vehicles     -> listar veiculos\n"
        "/vehicle <id> -> selecionar um veiculo\n"
        "/clean        -> limpar historico da conversa\n"
        "/clear        -> limpar historico da conversa\n"
        "/cls          -> limpar historico da conversa\n"
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

            previous_vehicle_id = application.vehicle_context.get_selected()

            if previous_vehicle_id != vehicle_id:
                application.conversation_context.clear()

            application.vehicle_context.select(
                vehicle_id
            )

            print(
                f"Veículo selecionado: {vehicle_id.value}"
            )
            print()
            continue

        if user_input.lower() in {"/clean", "/cls", "/clear"}:
            application.conversation_context.clear()
            print("Histórico da conversa limpo.\n")
            continue

        try:
            response = application.assistant.answer(user_input)
            print(response)
        except Exception as exc:
            print(f"Erro ao processar pergunta: {exc}")

        print()