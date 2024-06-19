# pysinergia\conectores\basedatos.py

import re
from abc import (ABC, ABCMeta, abstractmethod)
from datetime import (datetime, timedelta)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import ErrorPersonalizado

# --------------------------------------------------
# Interface: I_ConectorBasedatos
# --------------------------------------------------
class I_ConectorBasedatos(metaclass=ABCMeta):

    @abstractmethod
    def conectar(mi, config:dict) -> bool:
        ...

    @abstractmethod
    def desconectar(mi):
        ...

    @abstractmethod
    def crear_caso(mi, instruccion:str, parametros:list=[]) -> int:
        ...

    @abstractmethod
    def actualizar_caso(mi, instruccion:str, parametros:list=[]) -> int:
        ...

    @abstractmethod
    def eliminar_caso(mi, instruccion:str, parametros:list=[]) -> int:
        ...

    @abstractmethod
    def ver_caso(mi, instruccion:str, parametros:list=[], estructura:int=1) -> tuple:
        ...

    @abstractmethod
    def ver_lista(mi, instruccion:str, parametros:list=[], pagina:int=1, maximo:int=25, estructura:int=1) -> tuple:
        ...

    @abstractmethod
    def generar_comando(mi, plantilla:str, procedimiento:dict={}, campo_id:str='id') -> tuple:
        ...

    @abstractmethod
    def generar_consulta(mi, plantilla:str, procedimiento:dict={}) -> tuple:
        ...


# --------------------------------------------------
# Clase: ErrorBasedatos
# --------------------------------------------------
class ErrorBasedatos(ErrorPersonalizado):
    ...


# --------------------------------------------------
# Clase: Basedatos
# --------------------------------------------------
class Basedatos(ABC, I_ConectorBasedatos):
    def __init__(mi):
        mi.conexion = None
        mi.basedatos:str = None
        mi.ruta:str
        mi.marca:str
        mi._filtros = {
            mi.FILTRO.CONTIENE: mi._filtro_CONTIENE,
            mi.FILTRO.COINCIDE: mi._filtro_COINCIDE,
            mi.FILTRO.PALABRAS: mi._filtro_PALABRAS,
            mi.FILTRO.FRASE: mi._filtro_FRASE,
            mi.FILTRO.INCLUYE: mi._filtro_INCLUYE,
            mi.FILTRO.FECHA: mi._filtro_FECHA,
            mi.FILTRO.RANGO_FECHAS: mi._filtro_RANGO_FECHAS,
            mi.FILTRO.RANGO_NUMEROS: mi._filtro_RANGO_NUMEROS,
            mi.FILTRO.PERIODO: mi._filtro_PERIODO,
            mi.FILTRO.LISTA_DATOS: mi._filtro_LISTA_DATOS,
            mi.FILTRO.NUMERO: mi._filtro_NUMERO
        }

    # --------------------------------------------------
    # Clases de constantes

    class ESTRUCTURA:
        DICCIONARIO = 1
        TUPLA = 2

    class FILTRO:
        CONTIENE = "CONTIENE"
        COINCIDE = "COINCIDE"
        PALABRAS = "PALABRAS"
        FRASE = "FRASE"
        INCLUYE = "INCLUYE"
        FECHA = "FECHA"
        RANGO_FECHAS = "RANGO_FECHAS"
        RANGO_NUMEROS = "RANGO_NUMEROS"
        PERIODO = "PERIODO"
        LISTA_DATOS = "LISTA_DATOS"
        NUMERO = "NUMERO"

    class INSTRUCCION:
        SELECT_POR_ID = 'SELECT {lista_campos} FROM {origen_datos} WHERE id={id}'
        SELECT_CON_FILTROS = 'SELECT {mostrar} FROM {origen_datos} WHERE {filtrar} {ordenar}'
        INSERT_FILA = 'INSERT INTO {origen_datos} ({lista_campos}) VALUES ({lista_marcas})'
        UPDATE_POR_ID = 'UPDATE {origen_datos} SET {lista_campos} WHERE id={id}'
        DELETE_POR_ID = 'DELETE FROM {origen_datos} WHERE id={id}'

    class VALOR:
        NULO = 'F_NULO'
        VACIO = 'F_VACIO'
        NO_NULO = 'F_NO_NULO'
        HOY = 'F_HOY'
        AYER = 'F_AYER'
        ESTA_SEMANA = 'F_ESTA_SEMANA'
        ESTE_MES = 'F_ESTE_MES'
        ESTE_ANO = 'F_ESTE_ANO'
        ULTIMA_SEMANA = 'F_ULTIMA_SEMANA'
        ULTIMO_MES = 'F_ULTIMO_MES'
        ULTIMO_ANO = 'F_ULTIMO_ANO'
        SIGUIENTE_SEMANA = 'F_SIGUIENTE_SEMANA'
        SIGUIENTE_MES = 'F_SIGUIENTE_MES'
        SIGUIENTE_ANO = 'F_SIGUIENTE_ANO'
        ANTERIOR_SEMANA = 'F_ANTERIOR_SEMANA'
        ANTERIOR_MES = 'F_ANTERIOR_MES'
        ANTERIOR_ANO = 'F_ANTERIOR_ANO'

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

    def _crear_filtro(mi, filtro:str) -> str:
        return mi._filtros.get(filtro)

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
        if valor == mi.VALOR.NULO:
            expresion = f"( {campo} IS NULL )"
        elif valor == mi.VALOR.VACIO:
            expresion = f"( {campo} = '' )"
        elif valor == mi.VALOR.NO_NULO:
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
        if valor == mi.VALOR.NULO:
            expresion = f"( {campo} IS NULL )"
        elif valor == mi.VALOR.VACIO:
            expresion = f"( {campo} = '' )"
        elif valor == mi.VALOR.NO_NULO:
            expresion = f"( {campo} IS NOT NULL )"
        else:
            valor = valor.upper()
            expresion = f"((',' || UPPER({campo}) || ',') LIKE '%,{valor},%')"
        return expresion

    def _filtro_NUMERO(mi, campo:str, valor:str) -> str:
        valor = mi._limpiar_texto(valor)
        expresion = ""
        valor = valor.strip()
        if valor == mi.VALOR.NULO:
            expresion = f"( {campo} IS NULL )"
        elif valor == mi.VALOR.NO_NULO:
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
        valor = mi._limpiar_texto(valor)
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
        if valor == mi.VALOR.HOY:
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
            mi.VALOR.HOY: __periodo_hoy,
            mi.VALOR.AYER: __periodo_ayer,
            mi.VALOR.ESTA_SEMANA: __periodo_esta_semana,
            mi.VALOR.ESTE_MES: __periodo_este_mes,
            mi.VALOR.ESTE_ANO: __periodo_este_ano,
            mi.VALOR.ULTIMA_SEMANA: __periodo_ult_semana,
            mi.VALOR.ULTIMO_MES: __periodo_ult_mes,
            mi.VALOR.ULTIMO_ANO: __periodo_ult_ano,
            mi.VALOR.SIGUIENTE_SEMANA: __periodo_sig_semana,
            mi.VALOR.SIGUIENTE_MES: __periodo_sig_mes,
            mi.VALOR.SIGUIENTE_ANO: __periodo_sig_ano,
            mi.VALOR.ANTERIOR_SEMANA: __periodo_ant_semana,
            mi.VALOR.ANTERIOR_MES: __periodo_ant_mes,
            mi.VALOR.ANTERIOR_ANO: __periodo_ant_ano
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

    # --------------------------------------------------
    # Métodos públicos

    def desconectar(mi):
        if mi.conexion:
            mi.conexion.close()
            mi.conexion = None

    def crear_caso(mi, instruccion:str, parametros:list=[]) -> int:
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

    def generar_consulta(mi, plantilla:str=None, procedimiento:dict={}) -> tuple:
        if not plantilla or not procedimiento:
            return None
        mostrar:list[str] = []
        filtrar:list[str] = []
        ordenar:list[str] = []
        dto_solicitud_datos:dict = procedimiento.get('_dto_solicitud_datos', {})
        dto_origen_datos = procedimiento.get('_dto_origen_datos', '')
        pagina = int(dto_solicitud_datos.get('pagina', 1))
        maximo = int(dto_solicitud_datos.get('maximo', 25))
        plantilla = plantilla.replace('{origen_datos}', dto_origen_datos)
        for clave, contenido in dto_solicitud_datos.items():
            if isinstance(contenido, dict) and dto_origen_datos and clave not in ['_dto_contexto']:
                campo = contenido.get('campo', clave)
                entrada = contenido.get('entrada', '')
                salida = contenido.get('salida', '')
                entidad = contenido.get('entidad', '')
                filtro = contenido.get('filtro', '')
                orden = contenido.get('orden', '')
                valor = contenido.get('valor', '')
                if isinstance(valor, list):
                    valor = ','.join(valor)
                if entidad:
                    campo = f'{entidad}.{campo}'
                if orden:
                    ordenar.append(f'{campo} {orden}')
                if filtro and valor:
                    filtrado = mi._crear_filtro(filtro)(campo, valor)
                    if filtrado:
                        filtrar.append(filtrado)
        for clave, contenido in procedimiento.items():
            if isinstance(contenido, dict) and clave not in ['_dto_origen_datos','_dto_solicitud_datos','_dto_roles_sesion']:
                campo = clave
                entrada = contenido.get('entrada', '')
                salida = contenido.get('salida', '')
                entidad = contenido.get('entidad', '')
                if entidad:
                    salida = f'{entidad}.{salida}'
                campo_mostrar = f'{salida} as {entrada}' if entrada and salida != entrada else salida
                mostrar.append(campo_mostrar)
        mostrar_texto = ', '.join(mostrar) if mostrar else '*'
        plantilla = plantilla.replace('{mostrar}', mostrar_texto)
        filtrar_texto = ' AND '.join(filtrar) if filtrar else '1'
        plantilla = plantilla.replace('{filtrar}', filtrar_texto)
        ordenar_texto = ' ORDER BY ' + ', '.join(ordenar) if ordenar else ''
        plantilla = plantilla.replace('{ordenar}', ordenar_texto)
        return (plantilla, pagina, maximo)

    def generar_comando(mi, plantilla:str, procedimiento:dict={}, campo_id:str='id') -> tuple:
        if not plantilla or not procedimiento:
            return None

        def _formato_text(valor):
            return mi._limpiar_texto(valor)
        def _formato_integer(valor):
            return int(valor)
        def _formato_rounded(valor):
            return round(valor, None)
        def _formato_path(valor):
            return re.sub(r'\\', '/', valor)
        def _formato_strip(valor):
            return re.sub(r'-', ' ', valor).strip()
        def _formato_cleaned(valor):
            r = re.sub(r'\n', '|', valor)
            r = re.sub(r'\r', '', r)
            r = re.sub(r'"', "`", r)
            r = re.sub(r"'", "`", r)
            return r
        def _formato_sha256(valor):
            import hashlib
            if valor:
                sha256 = hashlib.sha256()
                sha256.update(str(valor).encode())
                hash_hex = sha256.hexdigest()
                return hash_hex
            return valor
        def _formato_decimal(valor):
            return valor
        formatos = {
            "text": _formato_text,
            "integer": _formato_integer,
            "rounded": _formato_rounded,
            "path": _formato_path,
            "strip": _formato_strip,
            "cleaned": _formato_cleaned,
            "sha256": _formato_sha256,
            "decimal": _formato_decimal
        }
        parametros:list = []
        campos:list[str] = []
        marcas:list[str] = []
        dto_solicitud_datos:dict = procedimiento.get('_dto_solicitud_datos', {})
        dto_origen_datos = procedimiento.get('_dto_origen_datos', '')
        plantilla = plantilla.replace('{origen_datos}', dto_origen_datos)
        for campo, contenido in procedimiento.items():
            if isinstance(contenido, dict) and not str(campo).startswith('_dto_') and dto_origen_datos:
                salida = contenido.get('salida', '')
                entidad = contenido.get('entidad', '')
                formato = contenido.get('formato', '')
                aux = dto_solicitud_datos.get(campo)
                valor = aux.get('valor', '') if aux and isinstance(aux, dict) else ''
                if valor:
                    if campo == campo_id:
                        plantilla = plantilla.replace('{id}', f"'{valor}'")
                    else:
                        if isinstance(valor, list):
                            valor = ','.join(valor)
                        if not entidad or entidad == dto_origen_datos:
                            if valor and formato:
                                valor = formatos.get(formato)(valor)
                        if plantilla.startswith('SELECT '):
                            campos.append(salida)
                        elif plantilla.startswith('UPDATE ') and valor:
                            campos.append(f'{salida}={mi.marca}')
                            parametros.append(valor)
                        elif plantilla.startswith('INSERT ') and valor:
                            campos.append(salida)
                            marcas.append(mi.marca)
                            parametros.append(valor)
        lista_campos = ', '.join(campos) if campos else ''
        lista_marcas = ', '.join(marcas) if marcas else ''
        plantilla = plantilla.replace('{lista_campos}', lista_campos)
        plantilla = plantilla.replace('{lista_marcas}', lista_marcas)
        return (plantilla, parametros)

