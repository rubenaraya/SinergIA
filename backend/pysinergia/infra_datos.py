# backend\pysinergia\infra_datos.py

from abc import (ABCMeta, abstractmethod)

# --------------------------------------------------
# Interface: I_ConectorAlmacen
# --------------------------------------------------
class I_ConectorAlmacen(metaclass=ABCMeta):
    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorBasedatos
# --------------------------------------------------
class I_ConectorBasedatos(metaclass=ABCMeta):
    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorDisco
# --------------------------------------------------
class I_ConectorDisco(metaclass=ABCMeta):
    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorLlm
# --------------------------------------------------
class I_ConectorLlm(metaclass=ABCMeta):
    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


# --------------------------------------------------
# Interface: I_ConectorSpi
# --------------------------------------------------
class I_ConectorSpi(metaclass=ABCMeta):
    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...


