# backend\pysinergia\conectores\basedatos_mysql.py

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia import I_ConectorBasedatos as Basedatos

# --------------------------------------------------
# Clase: BasedatosMysql
# --------------------------------------------------
class BasedatosMysql(Basedatos):
    def __init__(mi):
        ...

    def conectar(mi, config:dict) -> bool:
        ...

    def desconectar(mi):
        ...

    def insertar(mi, sql:str, parametros:list) -> int:
        ...

    def actualizar(mi, sql:str, parametros:list) -> int:
        ...

    def eliminar(mi, sql:str, parametros:int) -> int:
        ...

    def leer(mi, sql:str, parametros:int, contenido:int) -> tuple:
        ...

    def obtener(mi, sql:str, parametros:list, pagina:int, maximo:int, contenido:int) -> tuple:
        ...

    def crear_filtro(mi, filtro:str) -> str:
        ...
