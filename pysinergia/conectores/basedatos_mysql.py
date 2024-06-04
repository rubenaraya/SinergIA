# pysinergia\conectores\basedatos_mysql.py

# --------------------------------------------------
# Importaciones de Infraestructura de Datos
import re
from mysql.connector import connect, MySQLConnection, Error
from datetime import (datetime, timedelta)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_ConectorBasedatos as _Basedatos

# --------------------------------------------------
# Clase: BasedatosMysql
# --------------------------------------------------
class BasedatosMysql(_Basedatos):
    def __init__(mi):
        mi.conexion:MySQLConnection = None
        mi.basedatos:str = None
        mi.filtros = {
            _Basedatos.FILTRO.CONTIENE: mi._filtro_CONTIENE,
            _Basedatos.FILTRO.COINCIDE: mi._filtro_COINCIDE,
            _Basedatos.FILTRO.PALABRAS: mi._filtro_PALABRAS,
            _Basedatos.FILTRO.FRASE: mi._filtro_FRASE,
            _Basedatos.FILTRO.INCLUYE: mi._filtro_INCLUYE,
            _Basedatos.FILTRO.FECHA: mi._filtro_FECHA,
            _Basedatos.FILTRO.RANGO_FECHAS: mi._filtro_RANGO_FECHAS,
            _Basedatos.FILTRO.RANGO_NUMEROS: mi._filtro_RANGO_NUMEROS,
            _Basedatos.FILTRO.PERIODO: mi._filtro_PERIODO,
            _Basedatos.FILTRO.LISTA_DATOS: mi._filtro_LISTA_DATOS,
            _Basedatos.FILTRO.NUMERO: mi._filtro_NUMERO
        }

    # --------------------------------------------------
    # Métodos públicos

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
                    print(e)
        return False

    def desconectar(mi):
        if mi.conexion:
            mi.conexion.close()
            mi.conexion = None

    def obtener(mi, instruccion:str, parametros:list=[], pagina:int=1, maximo:int=25, contenido:int=_Basedatos.ESTRUCTURA.DICCIONARIO) -> tuple:
        cursor = mi.conexion.cursor()
        instruccion = instruccion.replace(' ? ', ' %s ')
        sql_total = f"SELECT COUNT(*) FROM ({instruccion}) as aux"
        cursor.execute(sql_total, parametros)
        total = cursor.fetchone()[0]
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
        if contenido == _Basedatos.ESTRUCTURA.DICCIONARIO:
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
            return datos, total
        elif contenido == _Basedatos.ESTRUCTURA.TUPLA:
            return (cursor.fetchall(), total)

    def leer(mi, instruccion:str, parametros:list, contenido:int=_Basedatos.ESTRUCTURA.DICCIONARIO) -> tuple:
        instruccion = instruccion.replace(' ? ', ' %s ')
        if contenido == _Basedatos.ESTRUCTURA.DICCIONARIO:
            cursor = mi.conexion.cursor(dictionary=True)
            cursor.execute(instruccion, parametros)
            lista = [dict(fila) for fila in cursor.fetchall()]
            return lista[0], 1
        elif contenido == _Basedatos.ESTRUCTURA.TUPLA:
            cursor = mi.conexion.cursor()
            cursor.execute(instruccion, parametros)
            return (cursor.fetchone(), 1)

    def insertar(mi, instruccion:str, parametros:list) -> int:
        instruccion = instruccion.replace(' ? ', ' %s ')
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        mi.conexion.commit()
        return cursor.lastrowid

    def actualizar(mi, instruccion:str, parametros:list) -> int:
        instruccion = instruccion.replace(' ? ', ' %s ')
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        mi.conexion.commit()
        return cursor.rowcount

    def eliminar(mi, instruccion:str, parametros:list) -> int:
        instruccion = instruccion.replace(' ? ', ' %s ')
        cursor = mi.conexion.cursor()
        sql_total = instruccion.replace('DELETE FROM ', 'SELECT COUNT(*) FROM ')
        cursor.execute(sql_total, parametros)
        total = cursor.fetchone()[0]
        if total > 0:
            cursor.execute(instruccion, parametros)
            mi.conexion.commit()
        return total

    def crear_filtro(mi, filtro:str) -> str:
        return mi.filtros.get(filtro)

    # --------------------------------------------------
    # Métodos privados

    def _limpiar_texto(mi, texto:str) -> str:
        texto = re.sub(r'[\']', "", str(texto))
        texto = re.sub(r"[\x00\x0A\x0D\x1A\x22\x27\x5C]", lambda m: '\\' + m.group(0), texto)
        return texto

    def _limpiar_numero(mi, numero:str, decimales:int=0) -> str:
        from decimal import Decimal, InvalidOperation
        numero = re.sub(r',', '.', numero)
        numero = numero.strip()
        if len(re.findall(r'\.', numero)) > 1:
            return ''
        try:
            num = Decimal(numero)
        except InvalidOperation:
            return ''
        num = num.quantize(Decimal(10) ** -decimales)
        if num == num.to_integral():
            num = num.to_integral()
        numero = str(num)
        return numero

    def _limpiar_fecha(mi, fecha:str, salida:str='%Y-%m-%d') -> str:
        formatos = [ '%d-%m-%Y','%Y-%m-%d','%Y/%m/%d','%d/%m/%Y' ]
        fecha_valida = None
        for formato in formatos:
            try:
                fecha_valida = datetime.strptime(fecha, formato)
                break
            except ValueError:
                pass
        if fecha_valida:
            return str(fecha_valida.strftime(salida))
        else:
            return ''

    def _filtro_FRASE(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_PALABRAS(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_COINCIDE(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_CONTIENE(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_INCLUYE(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_NUMERO(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_RANGO_NUMEROS(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_RANGO_FECHAS(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_LISTA_DATOS(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_FECHA(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

    def _filtro_PERIODO(mi, campo:str, valor:str) -> str:
        raise NotImplementedError

