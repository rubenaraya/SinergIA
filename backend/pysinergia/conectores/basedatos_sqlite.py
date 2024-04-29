# backend\pysinergia\conectores\basedatos_sqlite.py

import databases

from backend.pysinergia import I_ConectorBasedatos as Basedatos

# --------------------------------------------------
# Clase: BasedatosSqlite
# --------------------------------------------------
class BasedatosSqlite(Basedatos):
    def __init__(mi):
        mi.conexion = None

    def conectar(mi, config:dict) -> bool:
        print("BasedatosSqlite.conectar")
        return True

    def desconectar(mi):
        if mi.conexion:
            mi.conexion.close()
            mi.conexion = None

    def insertar(mi, sql:str, parametros:list) -> int:
        ...

    def actualizar(mi, sql:str, parametros:list, uid:int) -> int:
        ...

    def eliminar(mi, sql:str, uid:int) -> int:
        ...

    def leer(mi, sql:str, uid:int, contenido:int=Basedatos.CONTENIDO.DICCIONARIO) -> tuple:
        ...

    def obtener(mi, sql:str, parametros:list, contenido:int=Basedatos.CONTENIDO.DICCIONARIO, pag:int=1, max:int=25) -> tuple:
        ...
