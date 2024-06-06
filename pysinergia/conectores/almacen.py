# pysinergia\conectores\almacen.py

from abc import (ABC, ABCMeta, abstractmethod)

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
class ErrorAlmacen(Exception):
    def __init__(mi, mensaje:str, codigo:int=500, detalles:list=[]):
        mi.codigo = codigo
        mi.mensaje = mensaje
        mi.detalles = detalles
        super().__init__(mi.mensaje)

    def __str__(mi):
        return f'{mi.mensaje}'

    def __repr__(mi):
        return f'{mi.codigo}: {mi.mensaje} | {mi.detalles.__str__()}'


# --------------------------------------------------
# Clase: Almacen
# --------------------------------------------------
class Almacen(ABC, I_ConectorAlmacen):
    def __init__(mi):
        ...

