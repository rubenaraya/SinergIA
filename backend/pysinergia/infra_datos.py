import re, sqlite3
from backend.pysinergia.adaptadores import I_ConectorBasedatos

# --------------------------------------------------
# Colección de Conectores
# --------------------------------------------------

class BasedatosSqlite(I_ConectorBasedatos):
    def __init__(mi):
        ...
    def conectar(mi):
        print("BasedatosSqlite.conectar")
        ...
    def insertar(mi):
        ...
    def actualizar(mi):
        ...
    def eliminar(mi):
        ...
    def recuperar(mi):
        ...
