import re

from slm_assistentemanutencaocarro.domain.vehicle_answer import VehicleAnswer


class ResponseValidationService:
    
    def validate(
        self,
        answer: VehicleAnswer,
        response: str,
    ) -> bool:
        expected_values = self._extract_values(answer.answer)
        response_values = self._extract_values(response)

        return expected_values.issubset(response_values)

    def _extract_values(self, text: str) -> set[str]:
        values = set()

        values.update(
            value.upper()
            for value in re.findall(
                r"\b\d+(?:[.,]\d+)?\s*(?:PSI|BAR)\b",
                text,
                re.IGNORECASE,
            )
        )

        values.update(
            value.upper()
            for value in re.findall(
                r"\b\d{3}/\d{2}\s*R\d{2}\b",
                text,
                re.IGNORECASE,
            )
        )

        values.update(
            value.upper()
            for value in re.findall(
                r"\b\d+W-\d+\b",
                text,
                re.IGNORECASE,
            )
        )

        return values