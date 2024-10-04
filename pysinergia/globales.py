# --------------------------------------------------
# pysinergia\globales.py
# --------------------------------------------------

import os
from typing import (
    Tuple,
    Union,
    Any,
)

# --------------------------------------------------
# Clase estática: Constantes
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class Constantes:

    def __new__(cls):
        raise TypeError('No-se-puede-instanciar-una-clase-estatica')

    class ENTORNO:
        PRODUCCION = 'PRODUCCION'
        DESARROLLO = 'DESARROLLO'
        PRUEBAS = 'PRUEBAS'
        LOCAL = 'LOCAL'

    class REGISTRO:
        INFO = 'INFO'
        DEBUG = 'DEBUG'
        WARNING = 'WARNING'
        ERROR = 'ERROR'
        CRITICAL = 'CRITICAL'

    class CONCLUSION:
        EXITO = "EXITO"
        AVISO = "AVISO"
        ALERTA = "ALERTA"
        ERROR = "ERROR"

    class ESTADO:
        _200_EXITO = 200
        _201_CREADO = 201
        _204_VACIO = 204
        _300_AVISO = 300
        _302_REDIRIGIDO = 302
        _400_NO_VALIDO = 400
        _401_NO_AUTENTICADO = 401
        _403_NO_AUTORIZADO = 403
        _404_NO_ENCONTRADO = 404
        _405_NO_PERMITIDO = 405
        _410_NO_CONTINUADO = 410
        _413_NO_CARGADO = 413 # Request Entity Too Large
        _415_NO_SOPORTADO = 415 # Unsupported Media Type
        _422_NO_PROCESABLE = 422 # Unprocessable Entity
        _429_NO_ATENDIDO = 429 # Too Many Requests
        _500_ERROR = 500
        _503_NO_DISPONIBLE = 503
        _504_NO_RESPONDIDO = 504

    class MIME:
        HTML = 'text/html'
        JSON = 'application/json'
        MANIFEST = 'application/manifest+json'
        TXT = 'text/plain'
        BIN = 'application/octet-stream'
        CSV = 'text/csv'
        JPG = 'image/jpg'
        JPEG = 'image/jpeg'
        PNG = 'image/png'
        JS = 'text/javascript'
        PDF = 'application/pdf'
        XML = 'application/xml'
        XHTML = 'application/xhtml+xml'
        ZIP = 'application/zip'
        XLS = 'application/vnd.ms-excel'
        XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        DOC = 'application/msword'
        DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        PPT = 'application/vnd.ms-powerpoint'
        PPTX = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        MP3 = 'audio/mpeg'
        MP4 = 'video/mpeg'
        OPUS = 'audio/opus'
        WEBM = 'video/webm'
        WEBA = 'audio/webm'
        WMA = 'audio/x-ms-wma'
        WMV = 'video/x-ms-wmv'
        OGG = 'audio/ogg'
        WAV = 'audio/wav'
        SVG = 'image/svg+xml'
        MD = 'text/markdown'

    class CONVERSION:
        PDF = 'PDF'
        WORD = 'WORD'
        EXCEL = 'EXCEL'
        CSV = 'CSV'
        HTML = 'HTML'
        JSON = 'JSON'
        TEXTO = 'TEXTO'
        PPTX = 'PPTX'

    class PESO:
        KB = 1024
        MB = 1024 * KB
        GB = 1024 * MB
        TB = 1024 * GB

    class TIEMPO:
        SEG = 1000
        MIN = 60 * SEG
        HOR = 60 * MIN
        DIA = 24 * HOR

    class AUDIO:
        WAV = 'wav'
        MP3 = 'mp3'
        MP4 = 'mp4'
        M4A = 'm4a'
        OGG = 'ogg'
        OPUS = 'opus'
        WMA = 'wma'
        WEBA = 'weba'
        WEBM = 'webm'

    class BITRATE:
        _64KBPS = '64'
        _96KBPS = '96'
        _128KBPS = '128'
        _192KBPS = '192'
        _256KBPS = '256'

    class CAMPO:
        CHECKBOX = 'checkbox'
        COLOR = 'color'
        DATE = 'date'
        EMAIL = 'email'
        HIDDEN = 'hidden'
        IMAGE = 'image'
        LABEL = 'label'
        NUMBER = 'number'
        PASSWORD = 'password'
        RADIO = 'radio'
        SEARCH = 'search'
        SELECT = 'select'
        SWITCH = 'switch'
        TEL = 'tel'
        TEXT = 'text'
        TEXTAREA = 'textarea'
        TIME = 'time'
        URL = 'url'

    class VALIDACION:
        TEXTO = 'texto'
        ENTERO = 'entero'
        DECIMAL = 'decimal'
        RUT = 'rut'
        OPCIONES = 'opciones'
        FECHA = 'fecha'
        NOVALIDAR = 'novalidar'

# --------------------------------------------------
# Clase estática: RegistradorLogs
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class RegistradorLogs:

    def __new__(cls):
        raise TypeError('No-se-puede-instanciar-una-clase-estatica')

    @staticmethod
    def crear(nombre:str, ruta_logs=None, nivel_registro:str=None):
        from logging import (Formatter, getLogger)
        from logging.handlers import RotatingFileHandler
        ruta_logs = ruta_logs if ruta_logs else os.getenv('RUTA_LOGS') if os.getenv('RUTA_LOGS') else 'logs'
        nivel_registro = nivel_registro if nivel_registro else os.getenv('NIVEL_REGISTRO') if os.getenv('NIVEL_REGISTRO') else Constantes.REGISTRO.ERROR
        registrador = getLogger(nombre)
        registrador.setLevel(nivel_registro)
        registrador.propagate = False
        manejador = RotatingFileHandler(
            filename = f'{ruta_logs}/{nombre}.log',
            maxBytes = (10 * (1048576)),
            backupCount = 9,
            encoding = 'utf-8'
        )
        manejador.setLevel(nivel_registro)
        manejador.setFormatter(Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s | %(module)s.%(funcName)s',
            datefmt="%Y-%m-%d %H:%M"
        ))
        registrador.addHandler(manejador)
        return registrador

# --------------------------------------------------
# Clase: ErrorPersonalizado
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class ErrorPersonalizado(Exception):
    def __init__(mi,
                mensaje:str,
                codigo:int=Constantes.ESTADO._500_ERROR,
                nivel_evento:str=Constantes.REGISTRO.ERROR,
                detalles:list=[],
                tipo:str='',
                recurso:str='',
                dominio_idioma:str=None,
                archivo_logs:str=None,
            ):
        mensaje = str(mensaje).replace('{','(').replace('}',')')
        super().__init__(mensaje)
        mi.mensaje:str = mensaje
        mi.codigo:int = int(codigo)
        mi.tipo:str = tipo
        mi.recurso:str = recurso
        mi.nivel_evento:str = nivel_evento
        mi.conclusion:str = mi._concluir(mi.codigo)
        mi.detalles:list = mi._detallar_errores(detalles) if detalles and isinstance(detalles, list) else []
        if not dominio_idioma:
            dominio_idioma = os.getenv('DOMINIO_IDIOMA', None) or 'base'
        mi.dominio_idioma:str = dominio_idioma
        if not archivo_logs:
            archivo_logs = os.getenv('ARCHIVO_LOGS', None) or 'app'
        mi.archivo_logs:str = archivo_logs

    def __str__(mi) -> str:
        return mi.mensaje

    def __repr__(mi) -> str:
        contenido = f'{mi.conclusion} {mi.codigo} | {mi.mensaje}'
        if mi.tipo:
            contenido = f'{contenido} ({mi.tipo})'
        if mi.recurso:
            contenido = f'{contenido} | {mi.recurso}'
        return contenido

    def _transformar_loc(mi, loc:Tuple[Union[str, int], ...]) -> str:
        path = ''
        for i, x in enumerate(loc):
            if isinstance(x, str):
                if i > 0:
                    path += '.'
                path += x
            elif isinstance(x, int):
                path += f'[{x}]'
        return path

    def _concluir(mi, estado:int) -> str:
        if estado < 200:
            return Constantes.CONCLUSION.ERROR
        if estado < 300:
            return Constantes.CONCLUSION.EXITO
        if estado < 400:
            return Constantes.CONCLUSION.AVISO
        if estado < 500:
            return Constantes.CONCLUSION.ALERTA
        return Constantes.CONCLUSION.ERROR

    def _detallar_errores(mi, errores:list) -> list:
        lista:list = []
        if errores and isinstance(errores, list):
            for error in errores:
                if isinstance(error, dict):
                    input = error.get('input', '')
                    valor = input if input and isinstance(input, (str, int, float, bool)) else ''
                    lista.append({
                        'clave': mi._transformar_loc(error.get('loc', [])),
                        'valor': valor,
                        'mensaje': '',
                        '_type': error.get('type', ''),
                        '_msg': error.get('msg', ''),
                        '_ctx': error.get('ctx', None)
                    })
        return lista

    def registrar(mi, exc_info:bool=None, texto_pre:str='', texto_pos:str='') -> str:
        if not exc_info:
            exc_info = bool(os.getenv('ENTORNO') == Constantes.ENTORNO.DESARROLLO)
        texto_registrado = mi.__repr__()
        texto_registrado = f'{texto_pre} | {texto_registrado}' if texto_pre else texto_registrado
        texto_registrado = f'{texto_registrado} | {texto_pos}' if texto_pos else texto_registrado
        registrador = RegistradorLogs.crear(mi.archivo_logs)
        if mi.nivel_evento == Constantes.REGISTRO.ERROR:
            registrador.error(texto_registrado, exc_info=exc_info)
        elif mi.nivel_evento == Constantes.REGISTRO.WARNING:
            registrador.warning(texto_registrado, exc_info=exc_info)
        elif mi.nivel_evento == Constantes.REGISTRO.DEBUG:
            registrador.debug(texto_registrado, exc_info=exc_info)
        elif mi.nivel_evento == Constantes.REGISTRO.INFO:
            registrador.info(texto_registrado, exc_info=exc_info)
        elif mi.nivel_evento == Constantes.REGISTRO.CRITICAL:
            registrador.critical(texto_registrado, exc_info=exc_info)
        return texto_registrado
    
    def exportar(mi) -> dict:
        return {
            'codigo': mi.codigo,
            'conclusion': mi.conclusion,
            'mensaje': mi.mensaje,
            'detalles': mi.detalles,
        }

# --------------------------------------------------
# Clase: ValidadorDatos
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class ValidadorDatos:
    def __init__(mi):
        mi.validaciones = {
            Constantes.VALIDACION.TEXTO: mi._validar_texto,
            Constantes.VALIDACION.ENTERO: mi._validar_entero,
            Constantes.VALIDACION.DECIMAL: mi._validar_decimal,
            Constantes.VALIDACION.FECHA: mi._validar_fecha,
            Constantes.VALIDACION.RUT: mi._validar_rut,
        }
        mi.errores:list = []

    # Métodos privados

    def _validar_texto(mi, minimo:float, maximo:float, valor:Any) -> bool:
        valor = str(valor).strip()
        if maximo > 0 and minimo <= len(valor) <= maximo:
            return True
        elif maximo == 0 and minimo <= len(valor):
            return True
        return False

    def _validar_entero(mi, minimo:float, maximo:float, valor:Any) -> bool:
        valor = int(valor)
        if maximo > 0 and minimo <= valor <= maximo:
            return True
        elif maximo == 0 and minimo <= valor:
            return True
        return False

    def _validar_decimal(mi, minimo:float, maximo:float, valor:Any) -> bool:
        valor = float(valor)
        if maximo > 0 and minimo <= valor <= maximo:
            return True
        elif maximo == 0 and minimo <= valor:
            return True
        return False

    def _validar_fecha(mi, minimo:float, maximo:float, valor:Any) -> bool:
        import datetime
        estado = False
        valor = str(valor)
        if len(valor) > 0 and '-' in valor:
            year, month, day = map(int, valor.split('-'))
            try:
                date = datetime.datetime(year, month, day)
                estado = True
                today = datetime.datetime.today()
                if maximo > 0 and date > today:
                    estado = False
                if minimo > 0 and date < today:
                    estado = False
            except Exception as e:
                print(e)
        elif minimo == 0 and maximo == 0 and len(valor) == 0:
            estado = True
        return estado

    def _validar_rut(mi, minimo:float, maximo:float, valor:Any) -> bool:
        valor = str(valor)
        if (minimo > 0 or len(valor) > 0) and '-' in valor:
            rut, dv = valor.split('-')
            if len(rut) > 0 and len(dv) == 1:
                m, s = 0, 1
                for digit in reversed(rut):
                    s = (s + int(digit) * (9 - m % 6)) % 11
                    m += 1
                calculated_dv = 'k' if s == 10 else str(s)
                if calculated_dv.lower() == dv.lower():
                    return True
        elif minimo == 0 and len(valor) == 0:
            return True
        return False

    def _validar_expreg(mi, patron:str, valor:Any) -> bool:
        import re
        valor = str(valor)
        try:
            if patron and len(valor) > 0:
                while patron.find('\\\\') >0:
                    patron = patron.replace('\\\\', '\\')
                expresion = re.compile('^' + patron + '$')
                if not expresion.match(valor):
                    return False
        except Exception as e:
            print(e)
        return True

    # Métodos públicos

    def verificar_campo(mi, criterios:dict, valor:Any) -> bool:
        if criterios.get('validacion') == 'novalidar':
            return True
        estado = False
        minimo = 0 if not criterios.get('minimo') else float(criterios.get('minimo'))
        maximo = 0 if not criterios.get('maximo') else float(criterios.get('maximo'))
        estado = mi.validaciones.get(criterios.get('validacion'))(minimo, maximo, valor)
        if estado:
            estado = mi._validar_expreg(criterios.get('patron', ''), valor)
        if not estado:
            mensaje = criterios.get('error', '')
            if len(mensaje) >0:
                mi.errores.append({
                    'campo': criterios.get('campo'),
                    'valor': valor,
                    'mensaje': mensaje,
                })
        return estado

# --------------------------------------------------
# Funcion: autorizar_acceso
"""
PROPOSITO:
RESPONSABILIDADES:
"""
def autorizar_acceso(roles:str, permisos:str=None) -> bool:
    if permisos == '':
        return True
    if permisos and roles:
        if permisos == '*':
            return True
        eval_permisos = set(permisos.split(','))
        eval_roles = set(roles.split(','))
        if bool(eval_permisos & eval_roles):
            return True
    return False

