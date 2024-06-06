# pysinergia\conectores\llm_openai.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.conectores.llm import (
    Llm as _Llm,
    ErrorLlm as _ErrorLlm
)

# --------------------------------------------------
# Clase: LlmOpenai
# --------------------------------------------------
class LlmOpenai(_Llm):
    def __init__(mi):
        super().__init__()
        ...

    def conectar(mi, config:dict) -> bool:
        return True

