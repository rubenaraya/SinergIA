# --------------------------------------------------
# pysinergia\conectores\basedatos_mysql.py
# --------------------------------------------------

from mysql.connector import (
    connect,
    MySQLConnection,
    Error,
)

# Importaciones de PySinergIA
from pysinergia.globales import (ErrorPersonalizado, Constantes)
from pysinergia.conectores.basedatos import Basedatos

# --------------------------------------------------
# Clase: BasedatosMysql
class BasedatosMysql(Basedatos):
    def __init__(mi):
        super().__init__()
        mi.conexion:MySQLConnection = None
        mi.marca_param = '%s'

    def _obtener_datos(mi, cursor) -> tuple:
        cursor = mi.conexion.cursor(dictionary=True)
        lista = [dict(fila) for fila in cursor.fetchall()]
        columnas = cursor.column_names
        return lista, columnas

    def conectar(mi, config:dict) -> bool:
        try:
            if mi.conexion and mi.basedatos == config.get('nombre'):
                return True
            if mi.conexion:
                mi.conexion.close()
            mi.basedatos = config.get('nombre')
            if mi.basedatos:
                mi.conexion = connect(
                    user=config.get('usuario'),
                    password=config.get('password'),
                    host=config.get('ruta'),
                    database=mi.basedatos
                )
                return mi.conexion.is_connected()
        except Error as e:
            raise ErrorPersonalizado(
                mensaje=str(e),
                codigo=Constantes.ESTADO._500_ERROR
            )
        return False

    def crear_tabla(mi, constructor:dict={}):
        return {}

