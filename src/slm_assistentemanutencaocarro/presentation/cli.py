from slm_assistentemanutencaocarro.infrastructure.composition import (
    create_assistant,
)


def run() -> None:
    assistant = create_assistant("data/vehicle.json")

    print("Assistente de Manutenção do Carro")
    print("Digite sua pergunta ou '/sair' para encerrar.")
    print()

    while True:
        question = input("> ").strip()

        if question.lower() in {"sair", "/exit", "/quit"}:
            print("Até mais!")
            break

        if not question:
            continue

        try:
            response = assistant.answer(question)
            print(response)
        except Exception as exc:
            print(f"Erro ao processar pergunta: {exc}")

        print()