# --------------------------------------------------
# pysinergia\conectores\basedatos_postgresql.py
# --------------------------------------------------

import psycopg2
from psycopg2.extras import RealDictCursor

# Importaciones de PySinergIA
from pysinergia.globales import (ErrorPersonalizado, Constantes)
from pysinergia.conectores.basedatos import Basedatos

# --------------------------------------------------
# Clase: BasedatosPostgresql
class BasedatosPostgresql(Basedatos):
    def __init__(mi):
        super().__init__()
        mi.marca_param = '%s'

    def _obtener_datos(mi, cursor) -> tuple:
        cursor = mi.conexion.cursor(cursor_factory=RealDictCursor)
        lista = [dict(fila) for fila in cursor.fetchall()]
        columnas = [desc[0] for desc in cursor.description]
        return lista, columnas

    def conectar(mi, config: dict) -> bool:
        try:
            if mi.conexion and mi.basedatos == config.get('nombre'):
                return True
            if mi.conexion:
                mi.conexion.close()
            mi.basedatos = config.get('nombre')
            mi.conexion = psycopg2.connect(
                dbname=mi.basedatos,
                user=config.get('usuario'),
                password=config.get('password'),
                host=config.get('ruta')
            )
            return True
        except psycopg2.Error as e:
            raise ErrorPersonalizado(
                mensaje=str(e),
                codigo=Constantes.ESTADO._500_ERROR
            )
        return False

