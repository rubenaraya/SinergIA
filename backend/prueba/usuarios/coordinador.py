# backend\prueba\usuarios\coordinador.py

from backend.pysinergia.nucleo import Coordinador

class CoordinadorUsuarios(Coordinador):
    def solicitar_accion(mi, accion:str) -> dict:
        ...
