import pytest

from benchmark.rag_refusal_detector import RagRefusalDetector


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        (
            "Não encontrei informações suficientes "
            "nos documentos disponíveis.",
            True,
        ),
        (
            "Não encontrei informações suficientes "
            "nos documentos disponíveis. [1] [2]",
            True,
        ),
        (
            "Não encontrei informações suficientes "
            "nos documentos disponíveis para responder à sua pergunta.",
            True,
        ),
        (
            "Consulte os dados do veículo selecionado [1].",
            False,
        ),
        (
            "Não, conhecer a viscosidade não permite "
            "concluir o intervalo de troca [1].",
            False,
        ),
        (
            'O exemplo de recusa é: "Não encontrei informações '
            'suficientes nos documentos disponíveis."',
            False,
        ),
    ],
)
def test_should_detect_refusal(response: str, expected: bool):
    assert RagRefusalDetector.detect(response) is expected
