# --------------------------------------------------
# pysinergia\conectores\basedatos_sqlite.py
# --------------------------------------------------

import os, sqlite3
from sqlite3 import Error
from pathlib import Path

# Importaciones de PySinergIA
from pysinergia.globales import *
from pysinergia.conectores.basedatos import Basedatos

# --------------------------------------------------
# Clase: BasedatosSqlite
class BasedatosSqlite(Basedatos):
    def __init__(mi):
        super().__init__()
        mi.conexion:sqlite3.Connection = None
        mi.marca_param = '?'
        mi.tipos = {
            'str': 'TEXT',
            'int': 'INTEGER',
            'float': 'REAL',
            'bool': 'INTEGER',
            'date': 'TEXT',
            'datetime': 'TEXT',
        }

    def _cargar_extension_sqlean(mi):
        try:
            mi.conexion.enable_load_extension(True)
            ruta_lib_sqlean = os.getenv('RUTA_LIB_SQLEAN')
            extension_lib_sqlean = Path(f'{ruta_lib_sqlean}/regexp').resolve()
            mi.conexion.load_extension(str(extension_lib_sqlean))
        except Exception as e:
            print(f"ERROR: {e}")

    def _obtener_datos(mi, cursor) -> tuple:
        cursor.row_factory = sqlite3.Row
        lista = [dict(fila) for fila in cursor.fetchall()]
        columnas = [desc[0] for desc in cursor.description]
        #columnas = list(map(lambda x: x[0], cursor.description))
        return (lista, columnas)

    def conectar(mi, config:dict) -> bool:
        try:
            if mi.conexion and mi.basedatos == config.get('nombre'):
                return True
            if mi.conexion:
                mi.conexion.close()
            mi.basedatos = config.get('nombre')
            mi.ruta = config.get('ruta')
            if mi.basedatos and mi.ruta:
                ruta_basedatos = Path(f"{mi.ruta}/{mi.basedatos}.db")
                if ruta_basedatos.is_file():
                    mi.conexion = sqlite3.connect(str(ruta_basedatos.resolve()))
                    mi._cargar_extension_sqlean()
                    return True
        except Error as e:
            raise ErrorPersonalizado(
                mensaje=str(e),
                codigo=Constantes.ESTADO._500_ERROR
            )
        return False

    def crear_tabla(mi, nombre:str, constructor:dict={}):
        try:
            columnas = ['id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT']
            sql_create_index = []
            for campo, detalles in constructor.items():
                tipo = detalles.get('tipo', 'str')
                largo = detalles.get('largo')
                default = detalles.get('default')
                indice = detalles.get('indice', '')
                tipo_sql = mi.tipos[tipo]
                if default is None:
                    default_sql = 'DEFAULT NULL'
                else:
                    default_sql = f"DEFAULT '{default}' NOT NULL"
                columna = f"{campo} {tipo_sql} {default_sql}"
                columnas.append(columna)
                if indice == 'simple':
                    sql_create_index.append(f"CREATE INDEX IF NOT EXISTS idx_{nombre}_{campo} ON {nombre} ({campo} ASC);")
                elif indice == 'unico':
                    sql_create_index.append(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{nombre}_{campo} ON {nombre} ({campo} ASC);")
            columnas_sql = ', '.join(columnas)
            sql_create_table = f"CREATE TABLE IF NOT EXISTS {nombre} ({columnas_sql});"
            cursor = mi.conexion.cursor()
            cursor.execute(sql_create_table)
            for sql in sql_create_index:
                cursor.execute(sql)
            mi.conexion.commit()
            return {'total': len(sql_create_index) + 1, 'create_table': sql_create_table, 'sql_create_index': sql_create_index}
        except Exception as e:
            raise ErrorPersonalizado(
                mensaje=str(e),
                codigo=Constantes.ESTADO._500_ERROR
            )

