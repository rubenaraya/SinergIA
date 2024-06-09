# pysinergia\__init__.py

import os
from pathlib import Path

# --------------------------------------------------
# Componentes Globales de PySinergIA
# --------------------------------------------------

__version__ = 'PySinergIA v0.0.1'

# --------------------------------------------------
# Clase estática: Constantes
# --------------------------------------------------
class Constantes:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    RUTA_CONECTORES = 'pysinergia.conectores'
    RUTA_EXPORTADORES = 'pysinergia.exportadores'
    DIR_LIB_SQLEAN = '_lib/sqlean'
    DIR_LIB_FFMPEG = '_lib/ffmpeg'
    DIR_LIB_PANDOC = '_lib/pandoc/bin'

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


# --------------------------------------------------
# Clase estática: RegistradorLogs
# --------------------------------------------------
class RegistradorLogs:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    @staticmethod
    def crear(nombre:str, ruta_logs='logs', nivel:str=Constantes.REGISTRO.ERROR):
        from logging import (Formatter, getLogger)
        from logging.handlers import RotatingFileHandler
        registrador = getLogger(nombre)
        registrador.setLevel(nivel)
        registrador.propagate = False
        manejador = RotatingFileHandler(
            filename = f'{ruta_logs}/{nombre}.log',
            maxBytes = (10 * (1048576)),
            backupCount = 9,
            encoding = 'utf-8'
        )
        manejador.setLevel(nivel)
        manejador.setFormatter(Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s | %(module)s.%(funcName)s',
            datefmt="%Y-%m-%d %H:%M"
        ))
        registrador.addHandler(manejador)
        return registrador


# --------------------------------------------------
# Clase: ErrorPersonalizado
# --------------------------------------------------
class ErrorPersonalizado(Exception):
    def __init__(mi, mensaje:str, codigo:int=500, detalles:list=[], aplicacion:str='', servicio:str='', recurso:str='', dominio_idioma:str='base', nivel_registro:str=Constantes.REGISTRO.ERROR):
        mi.codigo = int(codigo)
        mi.mensaje = str(mensaje).replace('{','(').replace('}',')')
        mi.detalles = detalles
        mi.aplicacion = aplicacion
        mi.servicio = servicio
        mi.recurso = recurso
        mi.dominio_idioma = dominio_idioma
        mi.nivel_registro = nivel_registro
        mi.conclusion = mi.concluir(mi.codigo)
        super().__init__(mi.mensaje)

    def __str__(mi):
        return mi.mensaje

    def __repr__(mi):
        contenido = f'{mi.conclusion} {mi.codigo} | {mi.mensaje}'
        if mi.aplicacion and mi.servicio:
            contenido = f'{mi.aplicacion}/{mi.servicio} | {contenido}'
        if mi.recurso:
            contenido = f'{contenido} | {mi.recurso}'
        return contenido

    def concluir(mi, estado:int) -> str:
        if estado < 200:
            return Constantes.CONCLUSION.ERROR
        if estado < 300:
            return Constantes.CONCLUSION.EXITO
        if estado < 400:
            return Constantes.CONCLUSION.AVISO
        if estado < 500:
            return Constantes.CONCLUSION.ALERTA
        return Constantes.CONCLUSION.ERROR

    def registrar(mi, nombre:str, texto_extra:str='', nivel_evento:str=Constantes.REGISTRO.ERROR, ruta_logs:str='logs') -> str:
        nombre = f'{mi.aplicacion}_{mi.servicio}' if mi.aplicacion and mi.servicio else nombre
        registro = mi.__repr__()
        registro = f'{texto_extra} | {registro}' if texto_extra else registro
        registrador = RegistradorLogs.crear(nombre=nombre, ruta_logs=ruta_logs, nivel=mi.nivel_registro)
        if nivel_evento == Constantes.REGISTRO.ERROR:
            registrador.error(registro)
        elif nivel_evento == Constantes.REGISTRO.WARNING:
            registrador.warning(registro)
        elif nivel_evento == Constantes.REGISTRO.DEBUG:
            registrador.debug(registro)
        elif nivel_evento == Constantes.REGISTRO.INFO:
            registrador.info(registro)
        elif nivel_evento == Constantes.REGISTRO.CRITICAL:
            registrador.critical(registro)
        return registro
    
    def serializar(mi) -> dict:
        return {
            'codigo': mi.codigo,
            'conclusion': mi.conclusion,
            'mensaje': mi.mensaje,
            'detalles': mi.detalles,
        }

    def agregar_detalles(mi, errores:list) -> list:
        if errores and isinstance(errores, list):
            for error in errores:
                if isinstance(error, dict):
                    type = error.get('type', '')
                    msg = error.get('msg', '')
                    loc = error.get('loc', '')
                    input = error.get('input', '')
                    if type or msg or loc or input:
                        mi.detalles.append({'type': type, 'msg': msg, 'loc': loc, 'input': input})
                    else:
                        print(error)
        return mi.detalles


# --------------------------------------------------
# Configuracion de FFMPEG
os.environ["PATH"] = str(Path(f'{Constantes.DIR_LIB_FFMPEG}').resolve()) + os.pathsep + os.getenv("PATH")

