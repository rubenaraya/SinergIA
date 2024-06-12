# pysinergia\conectores\llm.py

from abc import (ABC, ABCMeta, abstractmethod)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import ErrorPersonalizado

# --------------------------------------------------
# Interface: I_ConectorLlm
# --------------------------------------------------
class I_ConectorLlm(metaclass=ABCMeta):

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Clase: ErrorLlm
# --------------------------------------------------
class ErrorLlm(ErrorPersonalizado):
    ...


# --------------------------------------------------
# Clase: Llm
# --------------------------------------------------
class Llm(ABC, I_ConectorLlm):
    def __init__(mi):
        ...

