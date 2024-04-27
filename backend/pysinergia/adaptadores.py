# --------------------------------------------------
# Extensibles: Operador + Controlador
# --------------------------------------------------

from abc import (ABCMeta, abstractmethod)
from backend.pysinergia.servicios import I_Operador

# --------------------------------------------------

class I_ConectorBasedatos(metaclass=ABCMeta):
    @abstractmethod
    def conectar(mi):
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

class Operador(I_Operador):
    def __init__(mi):
        mi.basedatos:I_ConectorBasedatos
        ...

# --------------------------------------------------

class I_Emisor(metaclass=ABCMeta):
    @abstractmethod
    def entregar_respuesta(mi, resultado):
        ...

class I_Exportador(metaclass=ABCMeta):
    ...

class Controlador():
    def __init__(mi, emisor:I_Emisor):
        mi.emisor:I_Emisor = emisor
