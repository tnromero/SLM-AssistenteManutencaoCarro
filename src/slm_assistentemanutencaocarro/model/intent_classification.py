from pydantic import BaseModel

from slm_assistentemanutencaocarro.model.intent import Intent


class IntentClassification(BaseModel):
    intent: Intent
