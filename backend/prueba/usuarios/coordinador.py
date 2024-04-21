# backend\prueba\usuarios\coordinador.py

from backend.pysinergia.nucleo import Coordinador

# --------------------------------------------------
# SubClase: CoordinadorUsuarios
# --------------------------------------------------
class CoordinadorUsuarios(Coordinador):
    def solicitar_accion(mi, accion:str) -> dict:
        ...
