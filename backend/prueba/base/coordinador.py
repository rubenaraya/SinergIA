# backend\prueba\base\coordinador.py

from backend.pysinergia.nucleo import Coordinador

# --------------------------------------------------
# SubClase: CoordinadorBase
# --------------------------------------------------
class CoordinadorBase(Coordinador):
    def solicitar_accion(mi, accion:str) -> dict:
        ...
