# --------------------------------------------------
# pysinergia\conectores\basedatos.py
# --------------------------------------------------

from abc import (ABC, ABCMeta, abstractmethod)

# --------------------------------------------------
# Interface: I_ConectorBasedatos
class I_ConectorBasedatos(metaclass=ABCMeta):

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...

    @abstractmethod
    def desconectar(mi):
        ...

    @abstractmethod
    def agregar_caso(mi, instruccion:str, parametros:list=[]) -> int:
        ...

    @abstractmethod
    def actualizar_caso(mi, instruccion:str, parametros:list=[]) -> int:
        ...

    @abstractmethod
    def eliminar_caso(mi, instruccion:str, parametros:list=[]) -> int:
        ...

    @abstractmethod
    def abrir_caso(mi, instruccion:str, parametros:list=[]) -> dict:
        ...

    @abstractmethod
    def lista_casos(mi, instruccion:str, parametros:list=[], pagina:int=1, maximo:int=25) -> dict:
        ...

# --------------------------------------------------
# Clase: Basedatos
class Basedatos(ABC, I_ConectorBasedatos):
    def __init__(mi):
        mi.conexion = None
        mi.basedatos:str = None
        mi.ruta:str

    def desconectar(mi):
        if mi.conexion:
            mi.conexion.close()
            mi.conexion = None

    def agregar_caso(mi, instruccion:str, parametros:list=[]) -> int:
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        mi.conexion.commit()
        return cursor.lastrowid

    def actualizar_caso(mi, instruccion:str, parametros:list=[]) -> int:
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        mi.conexion.commit()
        return cursor.rowcount

    def eliminar_caso(mi, instruccion:str, parametros:list=[]) -> int:
        cursor = mi.conexion.cursor()
        sql_total = instruccion.replace('DELETE FROM ', 'SELECT COUNT(*) FROM ')
        cursor.execute(sql_total, parametros)
        total = cursor.fetchone()[0]
        if total > 0:
            cursor.execute(instruccion, parametros)
            mi.conexion.commit()
        return total

