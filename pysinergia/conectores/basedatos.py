# --------------------------------------------------
# pysinergia\conectores\basedatos.py
# --------------------------------------------------

from abc import ABC

# --------------------------------------------------
# Clase: Basedatos
class Basedatos(ABC):
    def __init__(mi):
        mi.conexion = None
        mi.basedatos:str = None
        mi.ruta:str

    def desconectar(mi):
        if mi.conexion:
            mi.conexion.close()
            mi.conexion = None

    def agregar_caso(mi, instruccion:str, parametros:list=[]) -> dict:
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        mi.conexion.commit()
        return {
            "id": cursor.lastrowid
        }

    def actualizar_caso(mi, instruccion:str, parametros:list=[]) -> dict:
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        mi.conexion.commit()
        return {
            "actualizados": cursor.rowcount
        }

    def eliminar_caso(mi, instruccion:str, parametros:list=[]) -> dict:
        cursor = mi.conexion.cursor()
        sql_total = instruccion.replace('DELETE FROM ', 'SELECT COUNT(*) FROM ')
        cursor.execute(sql_total, parametros)
        total = cursor.fetchone()[0]
        if total > 0:
            cursor.execute(instruccion, parametros)
            mi.conexion.commit()
        return {
            "eliminados": total
        }

