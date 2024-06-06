# pysinergia\conectores\spi.py

from abc import (ABC, ABCMeta, abstractmethod)

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
class ErrorSpi(Exception):
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
# Clase: Spi
# --------------------------------------------------
class Spi(ABC, I_ConectorSpi):
    def __init__(mi):
        ...

