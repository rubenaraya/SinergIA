# pysinergia\conectores\basedatos_sqlite.py

# --------------------------------------------------
# Importaciones de Infraestructura de Datos
import sqlite3, re
from datetime import (datetime, timedelta)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import Constantes as _Constantes
from pysinergia.adaptadores import I_ConectorBasedatos as _Basedatos

# --------------------------------------------------
# Clase: BasedatosSqlite
# --------------------------------------------------
class BasedatosSqlite(_Basedatos):
    def __init__(mi):
        mi.conexion:sqlite3.Connection = None
        mi.basedatos:str = None
        mi.ruta:str
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
        import os
        if mi.conexion and mi.basedatos == config.get('nombre'):
            return True
        if mi.conexion:
            mi.conexion.close()
        mi.basedatos = config.get('nombre')
        mi.ruta = config.get('ruta')
        if mi.basedatos and mi.ruta:
            ruta_basedatos = f"{mi.ruta}/{mi.basedatos}.db"
            if os.path.isfile(ruta_basedatos):
                mi.conexion = sqlite3.connect(ruta_basedatos)
                mi.conexion.enable_load_extension(True)
                extension = os.path.normpath(os.path.abspath(f"{_Constantes.DIR_LIB_SQLEAN}/regexp"))
                mi.conexion.load_extension(extension)
                return True
        return False

    def desconectar(mi):
        if mi.conexion:
            mi.conexion.close()
            mi.conexion = None

    def obtener(mi, instruccion:str, parametros:list=[], pagina:int=1, maximo:int=25, contenido:int=_Basedatos.FORMATO.DICCIONARIO) -> tuple:
        cursor = mi.conexion.cursor()
        sql_total = f"SELECT COUNT(*) FROM ({instruccion})"
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
            instruccion += " LIMIT ? OFFSET ?"
            parametros.extend([maximo, (pagina - 1) * maximo])
        cursor.execute(instruccion, parametros)
        if contenido == _Basedatos.FORMATO.DICCIONARIO:
            cursor.row_factory = sqlite3.Row
            lista = [dict(fila) for fila in cursor.fetchall()]
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
                "paginador": paginador
            }
            return datos, total
        elif contenido == _Basedatos.FORMATO.TUPLA:
            return (cursor.fetchall(), total)

    def leer(mi, instruccion:str, parametros:list, contenido:int=_Basedatos.FORMATO.DICCIONARIO) -> tuple:
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        if contenido == _Basedatos.FORMATO.DICCIONARIO:
            cursor.row_factory = sqlite3.Row
            lista = [dict(fila) for fila in cursor.fetchall()]
            return lista[0], 1
        elif contenido == _Basedatos.FORMATO.TUPLA:
            return (cursor.fetchone(), 1)

    def insertar(mi, instruccion:str, parametros:list) -> int:
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        mi.conexion.commit()
        return cursor.lastrowid

    def actualizar(mi, instruccion:str, parametros:list) -> int:
        cursor = mi.conexion.cursor()
        cursor.execute(instruccion, parametros)
        mi.conexion.commit()
        return cursor.rowcount

    def eliminar(mi, instruccion:str, parametros:list) -> int:
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
        valor = mi._limpiar_texto(valor)
        valor = valor.lower()
        valor = re.sub(r"['\"]", "", valor)
        valor = re.sub(r"\.", "", valor)
        valor = re.sub(r"  +", " ", valor)
        aux = valor.strip()
        aux = re.sub('[aáàäâ]', '(a|á|à|ä|â)', aux)
        aux = re.sub('[eéëèê]', '(e|é|è|ë|ê)', aux)
        aux = re.sub('[iíïìî]', '(i|í|ì|ï|î)', aux)
        aux = re.sub('[oóöòô]', '(o|ó|ò|ö|ô)', aux)
        aux = re.sub('[uúüùû]', '(u|ú|ù|ü|û)', aux)
        aux = re.sub('[ñ]', '(n|ñ)', aux)
        aux = re.sub('[ç]', '(c|ç)', aux)
        valor = valor.upper()
        expresion = f"( LOWER({campo}) regexp '[[:space:][:blank:]\",;:(+/¿¡=.-]{aux}[[:space:][:blank:]\",;:)+/?!=.-]' OR LOWER({campo}) regexp '^{aux}[[:space:][:blank:]\",;:())+/?!=.-]' OR LOWER({campo}) regexp '[[:space:][:blank:]\",;:())+/?!=.-]{aux}$' OR LOWER({campo}) regexp '^{aux}$' OR UPPER({campo}) LIKE '{valor}' )"
        return expresion

    def _filtro_PALABRAS(mi, campo:str, valor:str) -> str:
        valor = mi._limpiar_texto(valor)
        valor = valor.lower()
        valor = re.sub(r"['\"]", "", valor)
        valor = re.sub(r"\.", "", valor)
        valor = re.sub(r"  +", " ", valor)
        valor = valor.strip()
        lista = valor.split(" ")
        exp = []
        for palabra in lista:
            aux = palabra
            aux = re.sub('[aáàäâ]', '(a|á|à|ä|â)', aux)
            aux = re.sub('[eéëèê]', '(e|é|è|ë|ê)', aux)
            aux = re.sub('[iíïìî]', '(i|í|ì|ï|î)', aux)
            aux = re.sub('[oóöòô]', '(o|ó|ò|ö|ô)', aux)
            aux = re.sub('[uúüùû]', '(u|ú|ù|ü|û)', aux)
            aux = re.sub('[ñ]', '(n|ñ)', aux)
            aux = re.sub('[ç]', '(c|ç)', aux)
            exp.append(f"( LOWER({campo}) regexp '[[:space:][:blank:]\",;:()+/¿¡=.-]{aux}[[:space:][:blank:]\",;:())+/?!=.-]' OR LOWER({campo}) regexp '^{aux}[[:space:][:blank:]\",;:())+/?!=.-]' OR LOWER({campo}) regexp '[[:space:][:blank:]\",;:())+/?!=.-]{aux}$' OR LOWER({campo}) regexp '^{aux}$' )")
        expresion = ' AND '.join(exp)
        return expresion

    def _filtro_COINCIDE(mi, campo:str, valor:str) -> str:
        valor = mi._limpiar_texto(valor)
        if valor == "F_NULO":
            expresion = f"( {campo} IS NULL )"
        elif valor == "F_VACIO":
            expresion = f"( {campo} = '' )"
        elif valor == "F_NONULO":
            expresion = f"( {campo} IS NOT NULL )"
        else:
            valor = valor.lower()
            valor = re.sub(r"  +", " ", valor)
            valor = valor.strip()
            aux = re.sub('[aáàäâ]', '(a|á|à|ä|â)', valor)
            aux = re.sub('[eéëèê]', '(e|é|è|ë|ê)', aux)
            aux = re.sub('[iíïìî]', '(i|í|ì|ï|î)', aux)
            aux = re.sub('[oóöòô]', '(o|ó|ò|ö|ô)', aux)
            aux = re.sub('[uúüùû]', '(u|ú|ù|ü|û)', aux)
            aux = re.sub('[ñ]', '(n|ñ)', aux)
            aux = re.sub('[ç]', '(c|ç)', aux)
            valor = valor.upper()
            expresion = f"( LOWER({campo}) regexp '^{aux}$' OR UPPER({campo}) LIKE '{valor}' )"
        return expresion

    def _filtro_CONTIENE(mi, campo:str, valor:str) -> str:
        valor = mi._limpiar_texto(valor)
        aux = valor.lower()
        aux = re.sub(r'[aáàäâ]', '(a|á|à|ä|â)', aux)
        aux = re.sub(r'[eéëèê]', '(e|é|è|ë|ê)', aux)
        aux = re.sub(r'[iíïìî]', '(i|í|ì|ï|î)', aux)
        aux = re.sub(r'[oóöòô]', '(o|ó|ò|ö|ô)', aux)
        aux = re.sub(r'[uúüùû]', '(u|ú|ù|ü|û)', aux)
        aux = re.sub(r'[ñ]', '(n|ñ)', aux)
        aux = re.sub(r'[ç]', '(c|ç)', aux)
        valor = valor.upper()
        expresion = f"( LOWER({campo}) regexp '{aux}' OR UPPER({campo}) LIKE '%{valor}%' )"
        return expresion

    def _filtro_INCLUYE(mi, campo:str, valor:str) -> str:
        valor = mi._limpiar_texto(valor)
        if valor == "F_NULO":
            expresion = f"( {campo} IS NULL )"
        elif valor == "F_VACIO":
            expresion = f"( {campo} = '' )"
        elif valor == "F_NONULO":
            expresion = f"( {campo} IS NOT NULL )"
        else:
            valor = valor.upper()
            expresion = f"((',' || UPPER({campo}) || ',') LIKE '%,{valor},%')"
        return expresion

    def _filtro_NUMERO(mi, campo:str, valor:str) -> str:
        valor = mi._limpiar_texto(valor)
        expresion = ""
        valor = valor.strip()
        if valor == "F_NULO":
            expresion = f"( {campo} IS NULL )"
        elif valor == "F_NONULO":
            expresion = f"( {campo} IS NOT NULL )"
        else:
            valor = mi._limpiar_numero(valor)
            if valor:
                expresion = f"( {campo} = {valor} )"
        return expresion

    def _filtro_RANGO_NUMEROS(mi, campo:str, valor:str) -> str:
        valor = mi._limpiar_texto(valor)
        expresion = ""
        valor = valor.strip()
        valores = valor.split(",")
        if len(valores) == 2:
            desde = mi._limpiar_numero(valores[0])
            hasta = mi._limpiar_numero(valores[1])
            if desde and hasta:
                expresion = f"( {campo} BETWEEN '{desde}' AND '{hasta}' )"
        return expresion

    def _filtro_RANGO_FECHAS(mi, campo:str, valor:str) -> str:
        valor = mi._limpiar_texto(valor)
        expresion = ""
        valor = valor.strip()
        valores = valor.split(",")
        if len(valores) == 2:
            desde = mi._limpiar_fecha(valores[0], '%Y-%m-%d')
            hasta = mi._limpiar_fecha(valores[1], '%Y-%m-%d')
            if desde and hasta:
                expresion = f"( {campo} BETWEEN '{desde}' AND '{hasta}' )"
        return expresion

    def _filtro_LISTA_DATOS(mi, campo:str, valor:str) -> str:
        valor = mi.__limpiar_texto(valor)
        valor = valor.strip()
        valor = valor.replace('\n', '\r').replace('\r', ',').replace(' ', ',').replace(',,', ',')
        lista = [f"'{palabra.strip()}'" for palabra in valor.split(',') if len(palabra.strip()) > 0]
        valores = ','.join(lista)
        expresion = ""
        if len(valores) > 0:
            expresion = f"( {campo} IN ({valores}) )"
        return expresion

    def _filtro_FECHA(mi, campo:str, valor:str) -> str:
        valor = mi._limpiar_texto(valor)
        expresion = ""
        valor = valor.strip()
        if valor == "F_HOY":
            expresion = f"( {campo} = '{datetime.today().strftime('%Y-%m-%d')}' )"
        else:
            valor = mi._limpiar_fecha(valor, '%Y-%m-%d')
            if valor:
                expresion = f"( {campo} = '{valor}' )"
        return expresion

    def _filtro_PERIODO(mi, campo:str, valor:str) -> str:

        def __periodo_hoy(campo:str):
            fecha = datetime.now()
            hoy = fecha.strftime('%Y-%m-%d')
            return f"({campo} = '{hoy}')"
        def __periodo_ayer(campo:str):
            desde = ''
            fecha = datetime.now()
            fecha -= timedelta(days=1)
            desde = fecha.strftime('%Y-%m-%d')
            return f"({campo} = '{desde}')"
        def __periodo_esta_semana(campo:str):
            fecha = datetime.now()
            diasemana = fecha.weekday() + 1
            fecha -= timedelta(days=diasemana - 1)
            desde = fecha.strftime('%Y-%m-%d')
            fecha += timedelta(days=7 - diasemana)
            hasta = fecha.strftime('%Y-%m-%d')
            return f"({campo} BETWEEN '{desde}' AND '{hasta}')"
        def __periodo_este_mes(campo:str):
            fecha = datetime.now()
            mes = fecha.month
            ano = fecha.year
            return f"(strftime('%m', {campo}) = '{mes}' AND strftime('%Y', {campo}) = '{ano}')"
        def __periodo_este_ano(campo:str):
            fecha = datetime.now()
            ano = fecha.year
            return f"(strftime('%Y', {campo}) = '{ano}')"
        def __periodo_ult_semana(campo:str):
            fecha = datetime.now()
            hoy = fecha.strftime('%Y-%m-%d')
            fecha -= timedelta(weeks=1)
            desde = fecha.strftime('%Y-%m-%d')
            return f"({campo} BETWEEN '{desde}' AND '{hoy}')"
        def __periodo_ult_mes(campo:str):
            fecha = datetime.now()
            hoy = fecha.strftime('%Y-%m-%d')
            fecha -= timedelta(days=30)
            desde = fecha.strftime('%Y-%m-%d')
            return f"({campo} BETWEEN '{desde}' AND '{hoy}')"
        def __periodo_ult_ano(campo:str):
            fecha = datetime.now()
            hoy = fecha.strftime('%Y-%m-%d')
            fecha -= timedelta(days=365)
            desde = fecha.strftime('%Y-%m-%d')
            return f"({campo} BETWEEN '{desde}' AND '{hoy}')"
        def __periodo_sig_semana(campo:str):
            fecha = datetime.now()
            fecha += timedelta(weeks=1)
            hasta = fecha.strftime('%Y-%m-%d')
            fecha += timedelta(days=1)
            desde = fecha.strftime('%Y-%m-%d')
            return f"({campo} BETWEEN '{desde}' AND '{hasta}')"
        def __periodo_sig_mes(campo:str):
            fecha = datetime.now()
            fecha += timedelta(days=31)
            hasta = fecha.strftime('%Y-%m-%d')
            fecha += timedelta(days=1)
            desde = fecha.strftime('%Y-%m-%d')
            return f"({campo} BETWEEN '{desde}' AND '{hasta}')"
        def __periodo_sig_ano(campo:str):
            fecha = datetime.now()
            fecha += timedelta(days=365)
            hasta = fecha.strftime('%Y-%m-%d')
            fecha += timedelta(days=1)
            desde = fecha.strftime('%Y-%m-%d')
            return f"({campo} BETWEEN '{desde}' AND '{hasta}')"
        def __periodo_ant_semana(campo:str):
            fecha = datetime.now()
            fecha -= timedelta(weeks=1)
            diasemana = fecha.weekday() + 1
            fecha -= timedelta(days=diasemana - 1)
            desde = fecha.strftime('%Y-%m-%d')
            fecha += timedelta(days=7 - diasemana)
            hasta = fecha.strftime('%Y-%m-%d')
            return f"({campo} BETWEEN '{desde}' AND '{hasta}')"
        def __periodo_ant_mes(campo:str):
            fecha = datetime.now()
            aux = fecha.strftime('%Y-%m-') + '15'
            fecha = datetime.strptime(aux, '%Y-%m-%d')
            fecha -= timedelta(days=30)
            mes = fecha.month
            ano = fecha.year
            return f"(strftime('%m', {campo}) = '{mes}' AND strftime('%Y', {campo}) = '{ano}')"
        def __periodo_ant_ano(campo:str):
            fecha = datetime.now()
            aux = fecha.strftime('%Y-%m-') + '15'
            fecha = datetime.strptime(aux, '%Y-%m-%d')
            fecha -= timedelta(days=365)
            ano = fecha.year
            return f"(strftime('%Y', {campo}) = '{ano}')"

        periodos = {
            "F_HOY": __periodo_hoy,
            "F_AYER": __periodo_ayer,
            "F_ESTA_SEMANA": __periodo_esta_semana,
            "F_ESTE_MES": __periodo_este_mes,
            "F_ESTE_ANO": __periodo_este_ano,
            "F_ULT_SEMANA": __periodo_ult_semana,
            "F_ULT_MES": __periodo_ult_mes,
            "F_ULT_ANO": __periodo_ult_ano,
            "F_SIG_SEMANA": __periodo_sig_semana,
            "F_SIG_MES": __periodo_sig_mes,
            "F_SIG_ANO": __periodo_sig_ano,
            "F_ANT_SEMANA": __periodo_ant_semana,
            "F_ANT_MES": __periodo_ant_mes,
            "F_ANT_ANO": __periodo_ant_ano
        }
        exp = ''
        valor = mi._limpiar_texto(valor)
        valor = valor.strip()
        if valor.startswith("F_"):
            exp = periodos.get(valor)(campo)
        elif len(valor) == 6:
            ano = valor[:4]
            mes = valor[-2:]
            exp = f"(strftime('%m', {campo}) = '{mes}' AND strftime('%Y', {campo}) = '{ano}')"
        return exp

