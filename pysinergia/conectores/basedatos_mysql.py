# --------------------------------------------------
# pysinergia\conectores\basedatos_mysql.py
# --------------------------------------------------

from mysql.connector import (
    connect,
    MySQLConnection,
    Error,
)

# Importaciones de PySinergIA
from pysinergia.conectores.basedatos import (
    Basedatos,
)

# --------------------------------------------------
# Clase: BasedatosMysql
class BasedatosMysql(Basedatos):
    def __init__(mi):
        super().__init__()
        mi.marca = '%s'
        mi.conexion:MySQLConnection = None

    def conectar(mi, config:dict) -> bool:
        if mi.conexion and mi.basedatos == config.get('nombre'):
            return True
        if mi.conexion:
            mi.conexion.close()
        mi.basedatos = config.get('nombre')
        if mi.basedatos:
                try:
                    mi.conexion = connect(
                        user=config.get('usuario'),
                        password=config.get('password'),
                        host=config.get('ruta'),
                        database=mi.basedatos
                    )
                    return True
                except Error as e:
                    raise
        return False

    def lista_casos(mi, instruccion:str, parametros:list=[], pagina:int=1, maximo:int=25) -> dict:
        cursor = mi.conexion.cursor()
        sql_total = f"SELECT COUNT(*) FROM ({instruccion}) as aux"
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
            instruccion += " LIMIT %s OFFSET %s"
            parametros.extend([maximo, (pagina - 1) * maximo])
        cursor = mi.conexion.cursor(dictionary=True)
        cursor.execute(instruccion, parametros)
        lista = [dict(fila) for fila in cursor.fetchall()]
        columnas = cursor.column_names
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
        return datos

    def abrir_caso(mi, instruccion:str, parametros:list=[]) -> dict:
        cursor = mi.conexion.cursor(dictionary=True)
        cursor.execute(instruccion, parametros)
        caso = [dict(fila) for fila in cursor.fetchall()]
        if len(caso) > 0:
            return caso[0]
        return {}
