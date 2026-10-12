from pydantic import BaseModel

from slm_assistentemanutencaocarro.domain.question_type import QuestionType


class QuestionClassification(BaseModel):
    question_type: QuestionType
