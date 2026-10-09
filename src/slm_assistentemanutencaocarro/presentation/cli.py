from slm_assistentemanutencaocarro.application.application import Application
from slm_assistentemanutencaocarro.application.exception import (
    EmbeddingGenerationError,
    KnowledgeIndexNotReadyError,
    KnowledgeReadError,
    RagGenerationError,
    SessionPersistenceError,
)
from slm_assistentemanutencaocarro.domain.exception import VehicleNotFoundError
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId


def run(application: Application) -> None:

    print("Assistente de Manutenção")
    print("Comandos:")
    print(
        "/exit              -> sair do chat\n"
        "/quit              -> sair do chat\n"
        "/vehicles          -> listar veiculos\n"
        "/vehicle <id>      -> selecionar um veiculo\n"
        "/docs              -> listar documentos disponíveis\n"
        "/index             -> construir o índice de documentos\n"
        "/search <pergunta> -> pequisar trechos dos documentos\n"
        "/rag <pergunta>    -> responder usando documentos\n"
        "/clean             -> limpar historico da conversa\n"
        "/clear             -> limpar historico da conversa\n"
        "/cls               -> limpar historico da conversa\n"
        "/save              -> salvar veículo e historico\n"
        "/load              -> restaurar a sessao salva\n"
    )

    try:
        restored = application.session_service.restore()
    except SessionPersistenceError as exc:
        print(f"Não foi possível restaurar a sessão: {exc}")
    else:
        if restored:
            vehicle_id = application.vehicle_context.get_selected()

            if vehicle_id is None:
                print("Sessão restaurada sem veículo selecionado.")
            else:
                print(f"Sessão restaurada. Veículo: {vehicle_id.value}")

    while True:
        user_input = input("> ").strip()

        if user_input.lower() in {"/sair", "/exit", "/quit"}:
            print("Até mais!")
            break

        if user_input.lower() == "/save":
            try:
                application.session_service.save()
            except SessionPersistenceError as exc:
                print(f"Não foi possível salvar a sessão: {exc}")
            else:
                print("Sessão salva.")

            print()
            continue

        if user_input.lower() == "/load":
            try:
                restored = application.session_service.restore()
            except SessionPersistenceError as exc:
                print(f"Não foi possível carregar a sessão: {exc}")
            else:
                if restored:
                    print("Sessão carregada.")
                else:
                    print("Não existe sessão salva.")

            print()
            continue

        if user_input.lower() == "/docs":
            try:
                documents = application.knowledge_service.list_documents()
            except KnowledgeReadError as exc:
                print(f"Não foi possível listar os documentos: {exc}")
            else:
                if not documents:
                    print("Nenhum documento disponível.")

                for document in documents:
                    scope = (
                        document.vehicle_id.value
                        if document.vehicle_id is not None
                        else "geral"
                    )

                    print(
                        f"- {document.id}: {document.title} "
                        f"[{scope}] | Fonte: {document.source}"
                    )

            print()
            continue

        if user_input.lower() == "/index":
            try:
                count = application.knowledge_search_service.build_index()
            except (KnowledgeReadError, EmbeddingGenerationError, ValueError) as exc:
                print(f"Não foi possível indexar os documentos: {exc}")
            else:
                print(f"Índice preparado com {count} chunks.")

            print()
            continue

        command, _, argument = user_input.partition(" ")

        if command.lower() == "/search":
            question = argument.strip()

            if not question:
                print("Uso: /search <pergunta>\n")
                continue

            try:
                results = application.knowledge_search_service.search(
                    question=question,
                    top_k=3,
                )
            except (
                KnowledgeIndexNotReadyError,
                EmbeddingGenerationError,
                ValueError,
            ) as exc:
                print(f"Não foi possível pesquisar: {exc}")
            else:
                if not results:
                    print("Nenhum trecho disponível para o veículo ativo.")

                for position, result in enumerate(results, start=1):
                    chunk = result.chunk

                    print(f"\n{position}. {chunk.title}")
                    print(f"Similaridade: {result.score:.4f}")
                    print(f"Fonte: {chunk.source}")
                    print(f"Chunk: {chunk.id}")
                    print(chunk.content)

            print()
            continue

        if command.lower() == "/rag":
            question = argument.strip()

            if not question:
                print("Uso: /rag <pergunta>\n")
                continue

            try:
                answer = application.rag_service.answer(
                    question=question,
                    top_k=3,
                )
            except (
                KnowledgeIndexNotReadyError,
                EmbeddingGenerationError,
                RagGenerationError,
                ValueError,
            ) as exc:
                print(f"Não foi possível responder com documentos: {exc}")
            else:
                print(answer.response)

                if answer.results:
                    print("\nReferências recuperadas:")

                    for position, result in enumerate(answer.results, start=1):
                        chunk = result.chunk

                        print(
                            f"[{position}] {chunk.title} "
                            f"| Fonte: {chunk.source} "
                            f"| Chunk: {chunk.id}"
                        )

            print()
            continue
        
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
                application.vehicle_context.select(vehicle_id)
                _save_session(application)

            print(
                f"Veículo selecionado: {vehicle_id.value}"
            )
            print()
            continue

        if user_input.lower() in {"/clean", "/cls", "/clear"}:
            application.conversation_context.clear()
            _save_session(application)
            print("Histórico da conversa limpo.\n")
            continue

        

        try:
            response = application.assistant.answer(user_input)
        except Exception as exc:
            print(f"Erro ao processar pergunta: {exc}")
        else:
            print(response)
            _save_session(application)

        print()

def _save_session(application: Application) -> None:
    try:
        application.session_service.save()
    except SessionPersistenceError as exc:
        print(f"A sessão não foi salva: {exc}")
