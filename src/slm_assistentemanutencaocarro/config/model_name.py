from enum import Enum

# Modelo deterministico
RULE_BASED: str = "rule_based"

# Modelo Hibrido
HYBRID: str = "hybrid"

# Modelos de SLM
class OLLAMA_MODEL(str, Enum):
    LLAMA_3_2 = "llama3.2:1b"
    QWEN_3 = "qwen3:1.7b"
