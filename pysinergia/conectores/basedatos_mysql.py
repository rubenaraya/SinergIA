# pysinergia\conectores\basedatos_mysql.py

# --------------------------------------------------
# Importaciones de Infraestructura de Datos

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_ConectorBasedatos as _Basedatos

# --------------------------------------------------
# Clase: BasedatosMysql
# --------------------------------------------------
class BasedatosMysql(_Basedatos):
    def __init__(mi):
        ...
    def conectar(mi, config:dict) -> bool:
        return True

