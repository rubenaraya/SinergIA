# pysinergia\conectores\disco.py

from abc import (ABC, ABCMeta, abstractmethod)
from typing import (List, BinaryIO, TextIO)

# --------------------------------------------------
# Interface: I_ConectorDisco
# --------------------------------------------------
class I_ConectorDisco(metaclass=ABCMeta):

    @abstractmethod
    def normalizar_nombre(mi, nombre:str, extension:str=None, largo:int=100, auto:bool=False) -> str:
        ...

    @abstractmethod
    def generar_nombre(mi, nombre:str, unico:bool=True) -> str:
        ...

    @abstractmethod
    def escribir(mi, contenido: BinaryIO | TextIO, nombre:str, modo:str='') -> str:
        ...

    @abstractmethod
    def abrir(mi, nombre:str, modo:str='') -> BinaryIO | TextIO:
        ...

    @abstractmethod
    def eliminar(mi, nombre:str) -> bool:
        ...

    @abstractmethod
    def copiar(mi, nombre:str, dir_destino:str, mover:bool=False) -> bool:
        ...

    @abstractmethod
    def crear_carpeta(mi, nombre:str, antecesores:bool=False) -> str:
        ...

    @abstractmethod
    def eliminar_carpeta(mi, nombre:str) ->bool:
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


# --------------------------------------------------
# Clase: ErrorDisco
# --------------------------------------------------
class ErrorDisco(Exception):
    def __init__(mi, mensaje:str, ruta:str='', codigo:int=500, detalles:list=[]):
        mi.codigo = codigo
        mi.ruta = ruta
        mi.mensaje = mensaje
        mi.detalles = detalles
        super().__init__(mi.mensaje)

    def __str__(mi):
        return f'{mi.mensaje}'

    def __repr__(mi):
        return f'{mi.codigo}: {mi.mensaje} | {mi.ruta} | {mi.detalles.__str__()}'


# --------------------------------------------------
# Clase: Disco
# --------------------------------------------------
class Disco(ABC, I_ConectorDisco):
    def __init__(mi, config:dict):
        mi._config:dict = config or {}

