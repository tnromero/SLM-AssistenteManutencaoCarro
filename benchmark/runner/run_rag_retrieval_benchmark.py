from benchmark.benchmark.rag_retrieval_benchmark import (
    RagRetrievalBenchmark,
)
from benchmark.rag_dataset_loader import RagDatasetLoader
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.composition import (
    build_application,
)


def main() -> None:
    application = build_application("data/vehicle.json")
    application.vehicle_context.select(
        VehicleId(value="t-cross-2022")
    )

    dataset = RagDatasetLoader().load()
    search_service = application.knowledge_search_service

    # Aquecimento: fora das métricas.
    warmup_case = next(
        (case for case in dataset if case.answerable),
        None,
    )

    if warmup_case is not None:
        search_service.search(warmup_case.question, top_k=1)

    for top_k in (1, 3):
        result = RagRetrievalBenchmark.evaluate(
            search_service=search_service,
            dataset=dataset,
            top_k=top_k,
        )

        print(f"\n=== Recuperação — top_k={top_k} ===")
        print(result)

        for case in result.cases:
            print(
                f"{case.case_id}: "
                f"hit={case.hit} | "
                f"recall={case.recall:.2%} | "
                f"recuperados={case.retrieved_document_ids}"
            )


if __name__ == "__main__":
    main()