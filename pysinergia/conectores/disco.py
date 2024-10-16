# --------------------------------------------------
# pysinergia\conectores\disco.py
# --------------------------------------------------

from abc import (ABC, abstractmethod)
from typing import (BinaryIO, TextIO, List)

# Importaciones de PySinergIA
from pysinergia.globales import *

# --------------------------------------------------
# Clase: ErrorDisco
class ErrorDisco(ErrorPersonalizado):
    pass

# --------------------------------------------------
# Clase: Disco
class Disco(ABC):
    def __init__(mi, config:dict):
        mi._config:dict = config or {}

    @abstractmethod
    def generar_nombre(mi, nombre:str, unico:bool=False) -> str:
        ...

    @abstractmethod
    def normalizar_nombre(mi, nombre:str, extension:str=None, largo:int=100, auto:bool=False) -> str:
        ...

    @abstractmethod
    def eliminar(mi, nombre:str) -> bool:
        ...

    @abstractmethod
    def escribir(mi, contenido: BinaryIO | TextIO, nombre:str, modo:str='') -> str:
        ...

    @abstractmethod
    def abrir(mi, nombre:str, modo:str='') -> BinaryIO | TextIO:
        ...

    @abstractmethod
    def copiar(mi, nombre:str, dir_destino:str, mover:bool=False) -> bool:
        ...

    @abstractmethod
    def crear_carpeta(mi, nombre:str, antecesores:bool=False) -> str:
        ...

    @abstractmethod
    def eliminar_carpeta(mi, nombre:str) -> bool:
        ...

    @abstractmethod
    def comprobar_ruta(mi, nombre:str, tipo:str='') -> str:
        ...

    @abstractmethod
    def listar_archivos(mi, nombre:str, extension:str='*') -> List:
        ...

    @abstractmethod
    def empaquetar_zip(mi, dir_origen:str, ruta_archivo_zip:str) -> bool:
        ...

    @abstractmethod
    def extraer_zip(mi, ruta_archivo_zip:str, dir_destino:str) -> bool:
        ...

    @abstractmethod
    def convertir_imagen(mi, ruta_imagen:str, dir_destino:str, lista_salidas:list[dict]) -> list[str]:
        ...

__all__ = ['Disco', 'ErrorDisco']
