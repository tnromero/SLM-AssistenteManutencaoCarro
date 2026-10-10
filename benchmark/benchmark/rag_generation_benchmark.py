from time import perf_counter

from benchmark.model.rag_case import RagCase
from benchmark.model.rag_generation_case_result import (
    RagGenerationCaseResult,
)
from benchmark.rag_refusal_dector import RagRefusalDetector
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
from slm_assistentemanutencaocarro.application.service.rag_service import (
    RagService,
)


class RagGenerationBenchmark:
    @staticmethod
    def evaluate(
        search_service: KnowledgeSearchService,
        generator: RagResponseGenerator,
        validator: RagResponseValidationService,
        dataset: list[RagCase],
        top_k: int = 3,
    ) -> list[RagGenerationCaseResult]:
        if top_k < 1:
            raise ValueError("top_k deve ser maior que zero.")

        evaluations = []

        for case in dataset:
            results = ()
            response = None
            refused = None
            citations_valid = None
            refusal_format_valid = None
            retrieval_time = 0.0
            generation_time = 0.0
            error = None
            stage = "recuperação"

            try:
                start = perf_counter()

                try:
                    results = tuple(
                        search_service.search(
                            question=case.question,
                            top_k=top_k,
                        )
                    )
                finally:
                    retrieval_time = perf_counter() - start

                if not results:
                    response = RagService.NO_RESULTS_MESSAGE
                    refused = True
                else:
                    context = RagContext(
                        question=case.question,
                        results=results,
                    )

                    stage = "geração"
                    start = perf_counter()

                    try:
                        response = generator.generate(context)
                    finally:
                        generation_time = perf_counter() - start

                    refused = RagRefusalDetector.detect(response)

                    refusal_format_valid = (
                        response.strip()
                        == RagResponseValidationService.INSUFFICIENT_INFORMATION_MESSAGE  # noqa: E501
                        if refused
                        else None
                    )

                    citations_valid = validator.validate(
                        context,
                        response,
                    )

                    stage = "validação"
                    citations_valid = validator.validate(
                        context=context,
                        response=response,
                    )

            except Exception as exc:
                error = f"{stage}: {type(exc).__name__}: {exc}"

            evaluations.append(
                RagGenerationCaseResult(
                    case_id=case.id,
                    question=case.question,
                    answerable=case.answerable,
                    expected_answer=case.expected_answer,
                    retrieved_document_ids=tuple(
                        dict.fromkeys(
                            result.chunk.document_id for result in results
                        )
                    ),
                    response=response,
                    refused=refused,
                    citations_valid=citations_valid,
                    retrieval_time=retrieval_time,
                    generation_time=generation_time,
                    error=error,
                    refusal_format_valid=refusal_format_valid,
                )
            )

        return evaluations
