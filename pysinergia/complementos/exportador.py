# --------------------------------------------------
# pysinergia\complementos\exportador.py
# --------------------------------------------------

from abc import ABC
from pathlib import Path

# Importaciones de PySinergIA
from pysinergia.globales import ErrorPersonalizado

# --------------------------------------------------
# Clase: ErrorExportador
class ErrorExportador(ErrorPersonalizado):
    pass

# --------------------------------------------------
# Clase: Exportador
class Exportador(ABC):
    def __init__(mi, config_web:dict):
        mi.config_web:dict = config_web or {}

    def obtener_ruta(mi) -> str:
        ruta_temp = mi.config_web.get('RUTA_TEMP')
        ruta = Path(ruta_temp) / 'archivos'
        ruta = ruta.resolve()
        if not ruta.exists():
            return ''
        return ruta.as_posix()

