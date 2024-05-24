# pysinergia\conectores\disco_local.py

# --------------------------------------------------
# Importaciones de Infraestructura de Datos
import os, shutil
from typing import BinaryIO

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_ConectorDisco as _Disco
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
)

# --------------------------------------------------
# Clase: DiscoLocal
# --------------------------------------------------
class DiscoLocal(_Disco):
    def __init__(mi):
        mi.sobreescribir = True
        mi.ruta_base:str = None

    # --------------------------------------------------
    # Métodos privados

    def _comprobar_nombre(mi):
        ...

    # --------------------------------------------------
    # Métodos públicos

    def conectar(mi, config:dict) -> bool:
        return True

    def leer_nombre(mi, nombre:str) -> str:
        return ''

    def leer_ruta(mi, nombre:str) -> str:
        return ''

    def leer_peso(mi, nombre:str) -> int:
        return 0

    def abrir_archivo(mi, nombre:str, modo:str):
        return ''

    def escribir_archivo(mi, contenido, nombre:str, modo:str) -> str:
        return ''

    def crear_archivo(mi, nombre:str) -> str:
        return ''

    def eliminar_archivo(mi, nombre:str):
        return ''

    def copiar_archivo(mi, origen:str, destino:str):
        return ''

    def mover_archivo(mi, origen:str, destino:str):
        return ''

    def crear_carpeta(mi, nombre:str, ruta:str):
        return ''

    def eliminar_carpeta(mi, nombre:str):
        return ''


# --------------------------------------------------
# Clase: ArchivoLocal
# --------------------------------------------------
class ArchivoLocal:
    def __init__(mi):
        ...


