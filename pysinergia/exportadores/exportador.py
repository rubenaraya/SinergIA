# pysinergia\exportadores\exportador.py

from abc import (ABC, ABCMeta, abstractmethod)
from pathlib import Path

# --------------------------------------------------
# Interface: I_Exportador
# --------------------------------------------------
class I_Exportador(metaclass=ABCMeta):

    @abstractmethod
    def generar(mi, contenido:str='', opciones:dict={}):
        ...

    @abstractmethod
    def obtener_ruta(mi) -> str:
        ...


# --------------------------------------------------
# Clase: ErrorExportador
# --------------------------------------------------
class ErrorExportador(Exception):
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
# Clase: Exportador
# --------------------------------------------------
class Exportador(ABC, I_Exportador):
    def __init__(mi, config_web:dict):
        mi.config_web:dict = config_web or {}

    def obtener_ruta(mi) -> str:
        ruta_temp = mi.config_web.get('ruta_temp', '')
        ruta = Path(ruta_temp) / 'archivos'
        ruta = ruta.resolve()
        if not ruta.exists():
            return ''
        return ruta.as_posix()

