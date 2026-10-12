import argparse
import json
from collections import Counter
from pathlib import Path


VALID_VERDICTS = {
    "adequate",
    "partial",
    "unsupported",
    "incorrect",
    "unassessable",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.report.read_text(encoding="utf-8"))
    cases = payload["cases"]

    case_ids = [case["case_id"] for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("O relatório contém IDs de casos duplicados.")

    counts: Counter[str] = Counter()
    pending: list[str] = []
    problems: list[tuple[str, str, str]] = []

    for case in cases:
        review = case.get("manual_review", {})
        verdict = review.get("verdict")

        if verdict is None:
            pending.append(case["case_id"])
            continue

        if verdict not in VALID_VERDICTS:
            raise ValueError(
                f"Veredito inválido em {case['case_id']}: {verdict!r}"
            )

        counts[verdict] += 1

        if verdict != "adequate":
            problems.append(
                (
                    case["case_id"],
                    verdict,
                    review.get("notes", ""),
                )
            )

    reviewed = sum(counts.values())
    assessable = reviewed - counts["unassessable"]

    print(f"Modelo: {payload['model']}")
    print(f"Casos: {len(cases)}")
    print(f"Revisados: {reviewed}")
    print(f"Pendentes: {len(pending)}")

    for verdict in sorted(VALID_VERDICTS):
        print(f"{verdict}: {counts[verdict]}")

    if assessable:
        rate = counts["adequate"] / assessable
        print(f"Adequação entre casos avaliáveis revisados: {rate:.2%}")
    else:
        print("Adequação: não calculável.")

    if pending:
        print("\n=== Revisões pendentes ===")
        for case_id in pending:
            print(case_id)

    if problems:
        print("\n=== Casos com problemas ===")
        for case_id, verdict, notes in problems:
            print(f"{case_id}: {verdict}")
            print(f"  Motivo: {notes or 'Não informado.'}")


if __name__ == "__main__":
    main()
    