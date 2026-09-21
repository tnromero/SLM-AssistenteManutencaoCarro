from pydantic import BaseModel

from slm_assistentemanutencaocarro.config.model_name import OLLAMA_MODEL


class OllamaConfig(BaseModel):
    model_name:OLLAMA_MODEL
    think:bool = False
    temperature: float = 1.0