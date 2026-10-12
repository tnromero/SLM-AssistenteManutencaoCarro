import argparse
from datetime import UTC, datetime
from pathlib import Path

from benchmark.benchmark.rag_generation_benchmark import (
    RagGenerationBenchmark,
)
from benchmark.rag_dataset_loader import RagDatasetLoader
from benchmark.rag_generation_case_assessment import (
    RagGenerationCaseAssessment,
)
from benchmark.rag_generation_report_writer import RagGenerationReportWriter
from slm_assistentemanutencaocarro.application.model.rag_context import (
    RagContext,
)
from slm_assistentemanutencaocarro.config.settings import Settings
from slm_assistentemanutencaocarro.domain.vehicle_id import VehicleId
from slm_assistentemanutencaocarro.infrastructure.composition import (
    build_application,
)


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="rag_cases.json")
    args = parser.parse_args()

    application = build_application("data/vehicle.json")
    application.vehicle_context.select(
        VehicleId(value="t-cross-2022")
    )

    dataset = RagDatasetLoader().load(args.dataset)
    rag_service = application.rag_service

    # Aquecimento fora das métricas.
    warmup_results = tuple(
        application.knowledge_search_service.search(
            dataset[0].question,
            top_k=3,
        )
    )

    if warmup_results:
        rag_service.response_generator.generate(
            RagContext(
                question=dataset[0].question,
                results=warmup_results,
            )
        )

    results = RagGenerationBenchmark.evaluate(
        search_service=application.knowledge_search_service,
        generator=rag_service.response_generator,
        validator=rag_service.response_validator,
        dataset=dataset,
        top_k=3,
    )

    answerable = [result for result in results if result.answerable]
    unanswerable = [result for result in results if not result.answerable]

    undue_refusals = sum(
        result.refused is True and result.error is None
        for result in answerable
    )
    correct_refusals = sum(
        result.refused is True and result.error is None
        for result in unanswerable
    )
    errors = sum(result.error is not None for result in results)

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    report_path = Path(
        f"benchmark/result/rag-generation-{timestamp}.json"
    )

    RagGenerationReportWriter.write(
        report_path,
        model=Settings.ollama_rag_model,
        top_k=3,
        cases=results,
    )

    print(f"\nRelatório salvo: {report_path}")

    print(f"Casos: {len(results)}")
    print(f"Erros técnicos: {errors}")
    print(f"Recusas indevidas: {undue_refusals}/{len(answerable)}")
    print(f"Recusas corretas: {correct_refusals}/{len(unanswerable)}")

    print("\n=== Resultado por caso ===")

    for case in results:
        findings = RagGenerationCaseAssessment.assess(case)
        print(f"{case.case_id}: {' | '.join(findings)}")

    for result in results:
        print(f"\n=== {result.case_id} ===")
        print(f"Pergunta: {result.question}")
        expected_behavior = "RESPONDER" if result.answerable else "RECUSAR"
        findings = RagGenerationCaseAssessment.assess(result)
        print(f"Esperado: {expected_behavior}")
        print(f"Resultado: {' | '.join(findings)}")
        print(f"Respondível: {result.answerable}")
        print(f"Documentos: {result.retrieved_document_ids}")
        print(f"Referência: {result.expected_answer}")
        print(f"Resposta: {result.response}")
        if result.refused is True:
            print(f"Formato da recusa: {result.refusal_format_valid}")
        else:
            print(f"Validação de citações: {result.citations_valid}")
        print(f"Recuperação: {result.retrieval_time:.3f}s")
        print(f"Geração: {result.generation_time:.3f}s")
        print(f"Erro: {result.error}")


if __name__ == "__main__":
    main()
