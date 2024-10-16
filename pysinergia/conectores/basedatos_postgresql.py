# --------------------------------------------------
# pysinergia\conectores\basedatos_postgresql.py
# --------------------------------------------------

from psycopg2 import (connect, Error)
from psycopg2.extras import RealDictCursor

# Importaciones de PySinergIA
from pysinergia.globales import *
from pysinergia.conectores.basedatos import Basedatos

# --------------------------------------------------
# Clase: BasedatosPostgresql
class BasedatosPostgresql(Basedatos):
    def __init__(mi):
        super().__init__()
        mi.conexion = None
        mi.marca_param = '%s'
        mi.tipos = {
            'str': 'VARCHAR',
            'int': 'INTEGER',
            'float': 'REAL',
            'bool': 'BOOLEAN',
            'date': 'DATE',
            'datetime': 'TIMESTAMP',
        }

    def _obtener_datos(mi, cursor) -> tuple:
        cursor = mi.conexion.cursor(cursor_factory=RealDictCursor)
        lista = [dict(fila) for fila in cursor.fetchall()]
        columnas = [desc[0] for desc in cursor.description]
        return (lista, columnas)

    def conectar(mi, config: dict) -> bool:
        try:
            if mi.conexion and mi.basedatos == config.get('nombre'):
                return True
            if mi.conexion:
                mi.conexion.close()
            mi.basedatos = config.get('nombre')
            if mi.basedatos:
                mi.conexion = connect(
                    dbname=mi.basedatos,
                    user=config.get('usuario'),
                    password=config.get('password'),
                    host=config.get('ruta'),
                    port=config.get('puerto', 5432)
                )
                return True
        except Error as e:
            raise ErrorPersonalizado(
                mensaje=str(e),
                codigo=Constantes.ESTADO._500_ERROR
            )
        return False

    def crear_tabla(mi, nombre:str, constructor:dict={}):
        try:
            columnas = ['id SERIAL PRIMARY KEY']
            sql_create_index = []
            for campo, detalles in constructor.items():
                tipo = detalles.get('tipo', 'str')
                largo = detalles.get('largo')
                default = detalles.get('default')
                indice = detalles.get('indice', '')
                if tipo == 'str':
                    if largo and largo > 255:
                        tipo_sql = 'TEXT'
                    elif largo:
                        tipo_sql = f"VARCHAR({largo})"
                    else:
                        tipo_sql = 'VARCHAR(255)'
                else:
                    tipo_sql = mi.tipos.get(tipo, 'TEXT')
                if default is None:
                    default_sql = 'DEFAULT NULL'
                else:
                    default_sql = f"DEFAULT '{default}' NOT NULL"
                columna = f"{campo} {tipo_sql} {default_sql}"
                columnas.append(columna)
                if indice == 'simple':
                    sql_create_index.append(
                        f"CREATE INDEX IF NOT EXISTS idx_{nombre}_{campo} ON {nombre} ({campo} ASC);"
                    )
                elif indice == 'unico':
                    sql_create_index.append(
                        f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{nombre}_{campo} ON {nombre} ({campo} ASC);"
                    )
            columnas_sql = ', '.join(columnas)
            sql_create_table = f"CREATE TABLE IF NOT EXISTS {nombre} ({columnas_sql});"
            cursor = mi.conexion.cursor()
            cursor.execute(sql_create_table)
            for sql_index in sql_create_index:
                cursor.execute(sql_index)
            mi.conexion.commit()
            return {'total': len(sql_create_index) + 1, 'create_table': sql_create_table, 'sql_create_index': sql_create_index}
        except Exception as e:
            raise ErrorPersonalizado(
                mensaje=str(e),
                codigo=Constantes.ESTADO._500_ERROR
            )

