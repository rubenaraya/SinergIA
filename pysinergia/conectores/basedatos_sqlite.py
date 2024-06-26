# pysinergia\conectores\basedatos_sqlite.py

# --------------------------------------------------
# Importaciones de Infraestructura de Datos
import sqlite3

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import Constantes
from pysinergia.conectores.basedatos import (
    Basedatos,
    ErrorBasedatos,
)

# --------------------------------------------------
# Clase: BasedatosSqlite
# --------------------------------------------------
class BasedatosSqlite(Basedatos):
    def __init__(mi):
        super().__init__()
        mi.marca:str = '?'
        mi.conexion:sqlite3.Connection = None

    # --------------------------------------------------
    # Métodos públicos

    def conectar(mi, config:dict) -> bool:
        from pathlib import Path
        import os
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
                mi.conexion.enable_load_extension(True)
                ruta_lib_sqlean = os.getenv('RUTA_LIB_SQLEAN')
                extension_lib_sqlean = Path(f'{ruta_lib_sqlean}/regexp').resolve()
                if extension_lib_sqlean.is_file():
                    mi.conexion.load_extension(str(extension_lib_sqlean))
                return True
        return False

    def ver_lista(mi, instruccion:str, parametros:list=[], pagina:int=1, maximo:int=25, estructura:int=Basedatos.ESTRUCTURA.DICCIONARIO) -> tuple:
        cursor = mi.conexion.cursor()
        sql_total = f"SELECT COUNT(*) FROM ({instruccion})"
        cursor.execute(sql_total, parametros)
        total = cursor.fetchone()[0]
        if maximo < 1:
            maximo = 25
        if pagina < 1:
            pagina = 1
        paginas = (total + maximo - 1) // maximo
        primero = ((pagina - 1) * maximo) + 1
        ultimo = primero + (maximo - 1)
        if ultimo > total:
            ultimo = total
        if primero > ultimo:
            primero = ultimo
        if not " LIMIT " in instruccion and not " OFFSET " in instruccion:
            instruccion += " LIMIT ? OFFSET ?"
            parametros.extend([maximo, (pagina - 1) * maximo])
        cursor.execute(instruccion, parametros)
        if estructura == Basedatos.ESTRUCTURA.DICCIONARIO:
            cursor.row_factory = sqlite3.Row
            lista = [dict(fila) for fila in cursor.fetchall()]
            columnas = list(map(lambda x: x[0], cursor.description))
            paginador = []
            for pag in range(paginas):
                paginador.append(pag + 1)
            datos = {
                "total": total,
                "primero": primero,
                "ultimo": ultimo,
                "paginas": paginas,
                "pagina": pagina,
                "maximo": maximo,
                "lista": lista,
                "columnas": columnas,
                "paginador": paginador
            }
            return datos, total
        elif estructura == Basedatos.ESTRUCTURA.TUPLA:
            return (cursor.fetchall(), total)

    def ver_caso(mi, instruccion:str, parametros:list=[], estructura:int=Basedatos.ESTRUCTURA.DICCIONARIO) -> tuple:
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        if estructura == Basedatos.ESTRUCTURA.DICCIONARIO:
            cursor.row_factory = sqlite3.Row
            lista = [dict(fila) for fila in cursor.fetchall()]
            return lista[0], 1
        elif estructura == Basedatos.ESTRUCTURA.TUPLA:
            return (cursor.fetchone(), 1)

