# pysinergia\complementos\exportador.py

from abc import (ABC, ABCMeta, abstractmethod)
from pathlib import Path

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import ErrorPersonalizado

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
class ErrorExportador(ErrorPersonalizado):
    ...


# --------------------------------------------------
# Clase: Exportador
# --------------------------------------------------
class Exportador(ABC, I_Exportador):
    def __init__(mi, config_web:dict):
        mi.config_web:dict = config_web or {}

    def obtener_ruta(mi) -> str:
        ruta_temp = mi.config_web.get('RUTA_TEMP')
        ruta = Path(ruta_temp) / 'archivos'
        ruta = ruta.resolve()
        if not ruta.exists():
            return ''
        return ruta.as_posix()

