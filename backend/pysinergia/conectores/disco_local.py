# backend\pysinergia\conectores\disco_local.py

# --------------------------------------------------
# Importaciones de Infraestructura de Datos
import os

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia import I_ConectorDisco as Disco

# --------------------------------------------------
# Clase: DiscoLocal
# --------------------------------------------------
class DiscoLocal(Disco):
    def __init__(mi):
        ...
    def conectar(mi, config:dict) -> bool:
        return True
