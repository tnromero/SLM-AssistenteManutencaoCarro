import pytest
from pydantic import ValidationError

from slm_assistentemanutencaocarro.application.model.knowledge.vehicle_knowledge_search import (  # noqa: E501
    VehicleKnowledgeSearchRequest,
)


def make_request(**overrides):
    payload = {
        "vehicle_id": {"value": "vehicle-test"},
        "question": "Onde consultar a pressão?",
    }
    payload.update(overrides)
    return VehicleKnowledgeSearchRequest.model_validate(payload)


@pytest.mark.parametrize("question", ["", " ", "\n\t"])
def test_rejects_blank_question(question):
    with pytest.raises(ValidationError):
        make_request(question=question)


@pytest.mark.parametrize("top_k", [-1, 0, 11])
def test_rejects_top_k_outside_allowed_range(top_k):
    with pytest.raises(ValidationError):
        make_request(top_k=top_k)


@pytest.mark.parametrize("top_k", [1, 10])
def test_accepts_top_k_boundaries(top_k):
    assert make_request(top_k=top_k).top_k == top_k


def test_trims_question_and_defaults_top_k():
    request = make_request(question="  Onde consultar a pressão?  ")

    assert request.question == "Onde consultar a pressão?"
    assert request.top_k == 3


def test_rejects_unexpected_argument():
    with pytest.raises(ValidationError):
        make_request(unexpected=True)
