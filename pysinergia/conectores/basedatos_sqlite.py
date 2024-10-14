# --------------------------------------------------
# pysinergia\conectores\basedatos_sqlite.py
# --------------------------------------------------

import os
import sqlite3
from sqlite3 import Error
from pathlib import Path

# Importaciones de PySinergIA
from pysinergia.globales import (ErrorPersonalizado, Constantes)
from pysinergia.conectores.basedatos import Basedatos

# --------------------------------------------------
# Clase: BasedatosSqlite
class BasedatosSqlite(Basedatos):
    def __init__(mi):
        super().__init__()
        mi.conexion:sqlite3.Connection = None
        mi.marca_param = '?'

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
        columnas = [desc[0] for desc in cursor.description] #list(map(lambda x: x[0], cursor.description))
        return lista, columnas

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

