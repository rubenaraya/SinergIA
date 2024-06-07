# pysinergia\conectores\spi.py

from abc import (ABC, ABCMeta, abstractmethod)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import ErrorPersonalizado as _ErrorPersonalizado

# --------------------------------------------------
# Interface: I_ConectorSpi
# --------------------------------------------------
class I_ConectorSpi(metaclass=ABCMeta):

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Clase: ErrorSpi
# --------------------------------------------------
class ErrorSpi(_ErrorPersonalizado):
    ...


# --------------------------------------------------
# Clase: Spi
# --------------------------------------------------
class Spi(ABC, I_ConectorSpi):
    def __init__(mi):
        ...

