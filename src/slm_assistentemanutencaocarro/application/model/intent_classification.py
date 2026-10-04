from pydantic import BaseModel

from slm_assistentemanutencaocarro.domain.intent import Intent


class IntentClassification(BaseModel):
    intent: Intent
