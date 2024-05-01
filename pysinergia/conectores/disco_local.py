# pysinergia\conectores\disco_local.py

# --------------------------------------------------
# Importaciones de Infraestructura de Datos

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_ConectorDisco as Disco

# --------------------------------------------------
# Clase: DiscoLocal
# --------------------------------------------------
class DiscoLocal(Disco):
    def __init__(mi):
        ...
    def conectar(mi, config:dict) -> bool:
        return True
