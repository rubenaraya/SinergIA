# backend\pysinergia\conectores\basedatos_sqlite.py

from backend.pysinergia.interfaces import I_ConectorBasedatos

# --------------------------------------------------
# Clase: BasedatosSqlite
# --------------------------------------------------
class BasedatosSqlite(I_ConectorBasedatos):
    def __init__(mi):
        ...
    def conectar(mi, config:dict):
        return True
