# backend\pysinergia\conectores\basedatos_mysql.py

from backend.pysinergia import I_ConectorBasedatos

# --------------------------------------------------
# Clase: BasedatosMysql
# --------------------------------------------------
class BasedatosMysql(I_ConectorBasedatos):
    def __init__(mi):
        ...
    def conectar(mi, config:dict) -> bool:
        return True
