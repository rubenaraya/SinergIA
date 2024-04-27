from abc import (ABCMeta, abstractmethod)
from backend.pysinergia.servicios import I_Operador

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
    @abstractmethod
    def insertar(mi):
        ...
    @abstractmethod
    def actualizar(mi):
        ...
    @abstractmethod
    def eliminar(mi):
        ...
    @abstractmethod
    def recuperar(mi):
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


# --------------------------------------------------
# Clase: Operador
# --------------------------------------------------
class Operador(I_Operador):
    ...


# --------------------------------------------------
# Interface: I_Emisor
# --------------------------------------------------
class I_Emisor(metaclass=ABCMeta):
    @abstractmethod
    def entregar_respuesta(mi, resultado):
        ...


# --------------------------------------------------
# Interface: I_Exportador
# --------------------------------------------------
class I_Exportador(metaclass=ABCMeta):
    ...


# --------------------------------------------------
# Clase: Controlador
# --------------------------------------------------
class Controlador():
    def __init__(mi, emisor:I_Emisor):
        mi.emisor:I_Emisor = emisor
