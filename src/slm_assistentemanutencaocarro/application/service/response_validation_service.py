import re

from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class ResponseValidationService:
    
    def validate(
        self,
        answer: VehicleAnswer,
        generated_response: str,
    ) -> bool:
        expected_values = self._extract_factual_values(answer.answer)

        if not expected_values:
            return self._validate_text(
                expected_answer=answer.answer,
                generated_response=generated_response,
            )

        normalized_response = self._normalize_fact(generated_response)

        return all(
            self._normalize_fact(value) in normalized_response
            for value in expected_values
        )

    def _extract_factual_values(self, text: str) -> list[str]:
        patterns = [
            r"\b\d+(?:\.\d+)?\s?psi\b", # Pressao Pneu
            r"\b\d+(?:[.,]\d+)?\s?bar\b", # Pressao Pneu
            r"\b\d{3}/\d{2}\s?r\d{2}\b", # Tamanho Pneu
            r"\b\d{1,2}w-\d{2}\b", # Oleo 5w40
        ]

        values: list[str] = []

        for pattern in patterns:
            matches = re.findall(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            values.extend(matches)

        return values

    def _validate_text(
        self,
        expected_answer: str,
        generated_response: str,
    ) -> bool:
        expected = self._normalize_text(expected_answer)
        generated = self._normalize_text(generated_response)

        return expected in generated or generated in expected

    def _normalize_text(self, text: str) -> str:
        return " ".join(
            text.lower()
            .strip()
            .split()
        )

    def _normalize_fact(self, text: str) -> str:
        return (
            text.lower()
            .replace(",", ".")
            .replace(" ", "")
            .strip()
        )