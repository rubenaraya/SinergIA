# backend\prueba\base\coordinador.py

from backend.pysinergia.nucleo import Coordinador

class CoordinadorBase(Coordinador):
    def solicitar_accion(mi, accion:str) -> dict:
        ...
