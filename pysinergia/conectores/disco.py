# --------------------------------------------------
# pysinergia\conectores\disco.py
# --------------------------------------------------

from abc import ABC

# Importaciones de PySinergIA
from pysinergia.globales import ErrorPersonalizado

# --------------------------------------------------
# Clase: ErrorDisco
class ErrorDisco(ErrorPersonalizado):
    pass

# --------------------------------------------------
# Clase: Disco
class Disco(ABC):
    def __init__(mi, config:dict):
        mi._config:dict = config or {}

