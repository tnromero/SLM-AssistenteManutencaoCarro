from time import perf_counter

from benchmark.model.rag_case import RagCase
from benchmark.model.rag_retrieval_result import (
    RagRetrievalCaseResult,
    RagRetrievalResult,
)
from slm_assistentemanutencaocarro.application.service.knowledge_search_service import (  # noqa: E501
    KnowledgeSearchService,
)


class RagRetrievalBenchmark:
    @staticmethod
    def evaluate(
        search_service: KnowledgeSearchService,
        dataset: list[RagCase],
        top_k: int = 3,
    ) -> RagRetrievalResult:
        if top_k < 1:
            raise ValueError("top_k deve ser maior que zero.")

        case_results = []

        for case in dataset:
            if not case.answerable:
                continue

            start = perf_counter()
            results = search_service.search(
                question=case.question,
                top_k=top_k,
            )
            elapsed = perf_counter() - start

            retrieved_ids = tuple(dict.fromkeys(
                result.chunk.document_id for result in results
            ))

            expected_ids = set(case.expected_document_ids)
            matched_ids = expected_ids.intersection(retrieved_ids)

            case_results.append(
                RagRetrievalCaseResult(
                    case_id=case.id,
                    expected_document_ids=tuple(
                        case.expected_document_ids
                    ),
                    retrieved_document_ids=retrieved_ids,
                    hit=bool(matched_ids),
                    recall=len(matched_ids) / len(expected_ids),
                    elapsed=elapsed,
                )
            )

        return RagRetrievalResult(
            top_k=top_k,
            cases=tuple(case_results),
        )
