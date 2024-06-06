# pysinergia\conectores\almacen.py

from abc import (ABC, ABCMeta, abstractmethod)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import ErrorPersonalizado as _ErrorPersonalizado

# --------------------------------------------------
# Interface: I_ConectorAlmacen
# --------------------------------------------------
class I_ConectorAlmacen(metaclass=ABCMeta):

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Clase: ErrorAlmacen
# --------------------------------------------------
class ErrorAlmacen(_ErrorPersonalizado):
    ...


# --------------------------------------------------
# Clase: Almacen
# --------------------------------------------------
class Almacen(ABC, I_ConectorAlmacen):
    def __init__(mi):
        ...

