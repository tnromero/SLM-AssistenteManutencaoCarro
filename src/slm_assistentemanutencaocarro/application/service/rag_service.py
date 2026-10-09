from slm_assistentemanutencaocarro.application.exception import (
    RagGenerationError,
)
from slm_assistentemanutencaocarro.application.model.rag_answer import (
    RagAnswer,
)
from slm_assistentemanutencaocarro.application.model.rag_context import (
    RagContext,
)
from slm_assistentemanutencaocarro.application.port.rag_response_generator import (  # noqa: E501
    RagResponseGenerator,
)
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (  # noqa: E501
    KnowledgeSearchService,
)
from slm_assistentemanutencaocarro.application.service.rag_response_validation_service import (  # noqa: E501
    RagResponseValidationService,
)


class RagService:
    NO_RESULTS_MESSAGE = (
        "Não encontrei trechos disponíveis para responder essa pergunta."
    )

    def __init__(
        self,
        knowledge_search_service: KnowledgeSearchService,
        response_generator: RagResponseGenerator,
        response_validator: RagResponseValidationService,
    ):
        self.knowledge_search_service = knowledge_search_service
        self.response_generator = response_generator
        self.response_validator = response_validator

    def answer(
        self,
        question: str,
        top_k: int = 3,
    ) -> RagAnswer:
        if not question.strip():
            raise ValueError("A pergunta não pode ser vazia.")

        if top_k < 1:
            raise ValueError("top_k deve ser maior que zero.")

        results = tuple(
            self.knowledge_search_service.search(
                question=question,
                top_k=top_k,
            )
        )

        if not results:
            return RagAnswer(
                response=self.NO_RESULTS_MESSAGE,
                results=(),
            )

        context = RagContext(
            question=question,
            results=results,
        )

        response = self.response_generator.generate(context)

        if not self.response_validator.validate(
            context=context,
            response=response,
        ):
            raise RagGenerationError(
                "A resposta documental contém citações inválidas ou ausentes."
            )

        return RagAnswer(
            response=response,
            results=results,
        )
