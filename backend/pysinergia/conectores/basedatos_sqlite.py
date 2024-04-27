from backend.pysinergia.adaptadores import I_ConectorBasedatos

# --------------------------------------------------
# Clase: BasedatosSqlite
# --------------------------------------------------
class BasedatosSqlite(I_ConectorBasedatos):
    def __init__(mi):
        ...
    def conectar(mi, config:dict):
        print("BasedatosSqlite.conectar")
        return True
