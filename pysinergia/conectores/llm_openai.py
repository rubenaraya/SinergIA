# pysinergia\conectores\llm_openai.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.conectores.llm import (
    Llm,
    ErrorLlm,
)

# --------------------------------------------------
# Clase: LlmOpenai
# --------------------------------------------------
class LlmOpenai(Llm):
    def __init__(mi):
        super().__init__()
        ...

    def conectar(mi, config:dict) -> bool:
        return True

