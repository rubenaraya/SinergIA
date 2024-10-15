# --------------------------------------------------
# pysinergia\conectores\basedatos.py
# --------------------------------------------------

from abc import (ABC, abstractmethod)

# --------------------------------------------------
# Clase: Basedatos
class Basedatos(ABC):
    def __init__(mi):
        mi.basedatos:str = None
        mi.ruta:str
        mi.marca_param:str
        mi.conexion = None

    def __enter__(mi):
        return mi

    def __exit__(mi, exc_type, exc_val, exc_tb):
        mi.desconectar()

    @abstractmethod
    def conectar(mi, config: dict) -> bool:
        pass

    @abstractmethod
    def _obtener_datos(mi, cursor) -> tuple:
        pass

    def _calcular_paginacion(mi, total, pagina, maximo) -> tuple:
        if maximo < 1:
            maximo = 25
        if pagina < 1:
            pagina = 1
        paginas = (total + maximo - 1) // maximo
        primero = ((pagina - 1) * maximo) + 1
        ultimo = min(primero + maximo - 1, total)
        if ultimo > total:
            ultimo = total
        if primero > ultimo:
            primero = ultimo
        return primero, ultimo, paginas

    def desconectar(mi):
        if mi.conexion:
            mi.conexion.close()
            mi.conexion = None

    def lista_casos(mi, instruccion:str, parametros:list=[], pagina:int=1, maximo:int=25) -> dict:
        try:
            cursor = mi.conexion.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM ({instruccion})", parametros)
            total = cursor.fetchone()[0]
            primero, ultimo, paginas = mi._calcular_paginacion(total, pagina, maximo)
            instruccion_paginada = f"{instruccion} LIMIT {mi.marca_param} OFFSET {mi.marca_param}"
            parametros.extend([maximo, (pagina - 1) * maximo])
            cursor.execute(instruccion_paginada, parametros)
            lista, columnas = mi._obtener_datos(cursor)
            return {
                "total": total,
                "primero": primero,
                "ultimo": ultimo,
                "paginas": paginas,
                "pagina": pagina,
                "maximo": maximo,
                "lista": lista,
                "columnas": columnas,
                "paginador": list(range(1, paginas + 1))
            }
        except Exception as e:
            print(f"ERROR: {e}")
            return {"total": -1, "error": str(e)}

    def abrir_caso(mi, instruccion:str, parametros:list=[]) -> dict:
        try:
            cursor = mi.conexion.cursor()
            cursor.execute(instruccion, parametros)
            lista, columnas = mi._obtener_datos(cursor)
            total = len(lista)
            caso = lista[0] if total > 0 else {}
            return {
                "total": total,
                "caso": caso,
                "columnas": columnas
            }
        except Exception as e:
            print(f"ERROR: {e}")
            return {"total": -1, "error": str(e)}

    def agregar_caso(mi, instruccion:str, parametros:list=[]) -> dict:
        try:
            cursor = mi.conexion.cursor()
            cursor.execute(instruccion, parametros)
            mi.conexion.commit()
            return {"total": 1, "id": cursor.lastrowid}
        except Exception as e:
            print(f"ERROR: {e}")
            mi.conexion.rollback()
            return {"total": -1, "error": str(e)}

    def actualizar_caso(mi, instruccion:str, parametros:list=[]) -> dict:
        try:
            cursor = mi.conexion.cursor()
            cursor.execute(instruccion, parametros)
            mi.conexion.commit()
            return {"total": cursor.rowcount}
        except Exception as e:
            print(f"ERROR: {e}")
            mi.conexion.rollback()
            return {"total": -1, "error": str(e)}

    def eliminar_caso(mi, instruccion:str, parametros:list=[]) -> dict:
        try:
            cursor = mi.conexion.cursor()
            sql_total = instruccion.replace('DELETE FROM ', 'SELECT COUNT(*) FROM ')
            cursor.execute(sql_total, parametros)
            total = cursor.fetchone()[0]
            if total > 0:
                cursor.execute(instruccion, parametros)
                mi.conexion.commit()
            return {"total": total}
        except Exception as e:
            print(f"ERROR: {e}")
            mi.conexion.rollback()
            return {"total": -1, "error": str(e)}

    @abstractmethod
    def crear_tabla(mi, nombre:str, constructor:dict={}):
        ...

