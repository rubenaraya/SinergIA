# backend\pysinergia\conectores\basedatos_mysql.py

from backend.pysinergia import I_ConectorBasedatos as Basedatos

# --------------------------------------------------
# Clase: BasedatosMysql
# --------------------------------------------------
class BasedatosMysql(Basedatos):
    def __init__(mi):
        mi.conexion = None

    def conectar(mi, config:dict) -> bool:
        print("BasedatosMysql.conectar")
        return True

    def desconectar(mi):
        ...

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
