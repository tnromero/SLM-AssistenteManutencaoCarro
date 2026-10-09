from slm_assistentemanutencaocarro.application.application import Application
from slm_assistentemanutencaocarro.application.context.conversation_context import (  # noqa: E501
    ConversationContext,
)
from slm_assistentemanutencaocarro.application.context.vehicle_context import (
    VehicleContext,
)
from slm_assistentemanutencaocarro.application.service.assistant_service import (  # noqa: E501
    AssistantService,
)
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (  # noqa: E501
    KnowledgeSearchService,
)
from slm_assistentemanutencaocarro.application.service.knowledge_service import (  # noqa: E501
    KnowledgeService,
)
from slm_assistentemanutencaocarro.application.service.rag_response_validation_service import (  # noqa: E501
    RagResponseValidationService,
)
from slm_assistentemanutencaocarro.application.service.rag_service import (
    RagService,
)
from slm_assistentemanutencaocarro.application.service.response_validation_service import (  # noqa: E501
    ResponseValidationService,
)
from slm_assistentemanutencaocarro.application.service.session_service import (
    SessionService,
)
from slm_assistentemanutencaocarro.application.service.vehicle_query_service import (  # noqa: E501
    VehicleQueryService,
)
from slm_assistentemanutencaocarro.application.service.vehicle_service import (
    VehicleService,
)
from slm_assistentemanutencaocarro.config.settings import Settings
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_intent_classifier import (  # noqa: E501
    HybridIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_question_classifier import (  # noqa: E501
    HybridQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_question_resolver import (  # noqa: E501
    HybridQuestionResolver,
)
from slm_assistentemanutencaocarro.infrastructure.hybrid.hybrid_response_generator import (  # noqa: E501
    HybridResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.knowledge.in_memory_vector_index import (  # noqa: E501
    InMemoryVectorIndex,
)
from slm_assistentemanutencaocarro.infrastructure.knowledge.word_document_chunker import (  # noqa: E501
    WordDocumentChunker,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_embedding_generator import (  # noqa: E501
    OllamaEmbeddingGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_intent_classifier import (  # noqa: E501
    OllamaIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_classifier import (  # noqa: E501
    OllamaQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_question_resolver import (  # noqa: E501
    OllamaQuestionResolver,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_rag_response_generator import (  # noqa: E501
    OllamaRagResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.ollama.ollama_response_generator import (  # noqa: E501
    OllamaResponseGenerator,
)
from slm_assistentemanutencaocarro.infrastructure.persistence.json_session_repository import (  # noqa: E501
    JsonSessionRepository,
)
from slm_assistentemanutencaocarro.infrastructure.persistence.json_vehicle_reader import (  # noqa: E501
    JsonVehicleReader,
)
from slm_assistentemanutencaocarro.infrastructure.persistence.markdown_knowledge_reader import (  # noqa: E501
    MarkdownKnowledgeReader,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_intent_classifier import (  # noqa: E501
    RuleBasedIntentClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_classifier import (  # noqa: E501
    RuleBasedQuestionClassifier,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_question_resolver import (  # noqa: E501
    RuleBasedQuestionResolver,
)
from slm_assistentemanutencaocarro.infrastructure.rule_based.rule_based_response_generator import (  # noqa: E501
    RuleBasedResponseGenerator,
)


def build_application(json_file_vehicle: str) -> Application:

    settings = Settings()

    vehicle_reader = JsonVehicleReader(json_file_vehicle)

    intent_classifier = HybridIntentClassifier(
        rule_based_classifier=RuleBasedIntentClassifier(),
        ollama_classifier=OllamaIntentClassifier(model=settings.ollama_intent_model),
    )

    question_classifier = HybridQuestionClassifier(
        rule_classifier=RuleBasedQuestionClassifier(),
        slm_classifier=OllamaQuestionClassifier(model=settings.ollama_question_model),
    )

    response_generator = HybridResponseGenerator(
        response_generator=RuleBasedResponseGenerator(),
        fallback_generator=OllamaResponseGenerator(
            model=settings.ollama_response_model,
        ),
        response_validator=ResponseValidationService(),
    )

    vehicle_context = VehicleContext()
    vehicle_service = VehicleService(vehicle_reader, vehicle_context)
    vehicle_query_service = VehicleQueryService(vehicle_service)

    conversation_context = ConversationContext(max_turns=5)

    session_repository = JsonSessionRepository(
        path=settings.session_file,
    )

    session_service = SessionService(
        repository=session_repository,
        vehicle_reader=vehicle_reader,
        vehicle_context=vehicle_context,
        conversation_context=conversation_context,
    )

    question_resolver = HybridQuestionResolver(
        rule_question_resolver=RuleBasedQuestionResolver(),
        slm_question_resolver=OllamaQuestionResolver(
            model=settings.ollama_resolver_model,
            max_turns=5,
        ),
    )

    assistant = AssistantService(
        intent_classifier=intent_classifier,
        question_classifier=question_classifier,
        vehicle_query_service=vehicle_query_service,
        response_generator=response_generator,
        conversation_context=conversation_context,
        question_resolver=question_resolver,
    )

    knowledge_reader = MarkdownKnowledgeReader(
        manifest_path=settings.knowledge_manifest_file,
    )

    knowledge_service = KnowledgeService(
        knowledge_reader=knowledge_reader,
        vehicle_context=vehicle_context,
    )

    knowledge_search_service = KnowledgeSearchService(
        knowledge_reader=knowledge_reader,
        chunker=WordDocumentChunker(
            chunk_size=120,
            overlap=20,
        ),
        embedding_generator=OllamaEmbeddingGenerator(
            model=settings.ollama_embedding_model,
        ),
        vector_index=InMemoryVectorIndex(),
        vehicle_context=vehicle_context,
    )

    rag_service = RagService(
        knowledge_search_service=knowledge_search_service,
        response_generator=OllamaRagResponseGenerator(
            model=settings.ollama_rag_model,
        ),
        response_validator=RagResponseValidationService(),
    )

    return Application(
        assistant=assistant,
        vehicle_context=vehicle_context,
        vehicle_reader=vehicle_reader,
        conversation_context=conversation_context,
        session_service=session_service,
        knowledge_service=knowledge_service,
        knowledge_search_service=knowledge_search_service,
        rag_service=rag_service,
    )
