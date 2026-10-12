from benchmark.model.rag_generation_case_result import (
    RagGenerationCaseResult,
)


class RagGenerationCaseAssessment:
    @staticmethod
    def assess(case: RagGenerationCaseResult) -> tuple[str, ...]:
        if case.error is not None:
            return ("ERRO TÉCNICO",)

        if case.response is None or not case.response.strip():
            return ("RESPOSTA AUSENTE",)

        if case.refused is None:
            return ("RECUSA NÃO AVALIADA",)

        findings: list[str] = []

        if case.answerable and case.refused:
            findings.append("RECUSA INDEVIDA")
        elif not case.answerable and not case.refused:
            findings.append("RESPONDEU QUANDO DEVERIA RECUSAR")

        if case.refused:
            if case.refusal_format_valid is False:
                findings.append("FORMATO DA RECUSA INVÁLIDO")
            elif case.refusal_format_valid is None:
                findings.append("FORMATO DA RECUSA NÃO AVALIADO")
        else:
            if case.citations_valid is False:
                findings.append("CITAÇÕES INVÁLIDAS OU AUSENTES")
            elif case.citations_valid is None:
                findings.append("CITAÇÕES NÃO AVALIADAS")

        if findings:
            return tuple(findings)

        if case.refused:
            return ("RECUSA CORRETA",)

        return ("RESPOSTA COM CITAÇÕES VÁLIDAS — CONTEÚDO NÃO AVALIADO",)
