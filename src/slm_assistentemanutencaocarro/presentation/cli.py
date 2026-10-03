from slm_assistentemanutencaocarro.application.service.assistant_service import AssistantService


def run(assistant: AssistantService) -> None:

    print("Assistente de Manutenção")
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