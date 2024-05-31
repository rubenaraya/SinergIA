# pysinergia\__init__.py

import json, gettext
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

    class SALIDA:
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
        _413_NO_CARGADO = 413
        _415_NO_SOPORTADO = 415
        _422_NO_PROCESABLE = 422
        _429_NO_ATENDIDO = 429
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

    class FORMATO:
        PDF = 'PDF'
        WORD = 'WORD'
        EXCEL = 'EXCEL'
        CSV = 'CSV'
        HTML = 'HTML'
        JSON = 'JSON'
        TEXTO = 'TEXTO'

    class PESO:
        KB = 1024
        MB = 1024 * KB
        GB = 1024 * MB
        TB = 1024 * GB


# --------------------------------------------------
# Clase estática: Json
# --------------------------------------------------
class Json:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    @staticmethod
    def leer(archivo:str):
        data = None
        try:
            if archivo and Path(archivo).is_file():
                with open(archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
        except:
            pass
        return data

    @staticmethod
    def guardar(datos, archivo:str) -> bool:
        try:
            if archivo and datos:
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, ensure_ascii=False, indent=2)
                return True
        except:
            pass
        return False

    @staticmethod
    def codificar(objeto) -> str:
        return json.dumps(dict(objeto), ensure_ascii=False)

    @staticmethod
    def decodificar(texto:str):
        return json.loads(texto)


# --------------------------------------------------
# Clase estática: Funciones
# --------------------------------------------------
class Funciones:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    @staticmethod
    def fecha_hora(zona_horaria:str) -> dict:
        import pytz
        from datetime import datetime
        fechahora = {}
        if not zona_horaria:
            zona_horaria = 'Etc/GMT'
        ist = pytz.timezone(zona_horaria)
        local = ist.localize(datetime.now())
        fechahora['fecha'] = local.strftime( "%d/%m/%Y" )
        fechahora['hora'] = local.strftime( "%H:%M" )
        fechahora['hms'] = local.strftime( "%H:%M:%S" )
        fechahora['amd'] = local.strftime( "%Y-%m-%d" )
        fechahora['dma'] = local.strftime( "%d-%m-%Y" )
        fechahora['mda'] = local.strftime( "%m-%d-%Y" )
        fechahora['dm'] = local.strftime( "%d-%m" )
        fechahora['md'] = local.strftime( "%m-%d" )
        fechahora['ma'] = local.strftime( "%m-%Y" )
        fechahora['am'] = local.strftime( "%Y-%m" )
        fechahora['dia'] = local.strftime( "%d" )
        fechahora['mes'] = local.strftime( "%m" )
        fechahora['ano'] = local.strftime( "%Y" )
        fechahora['amdhms'] = local.strftime( "%Y%m%d%H%M%S" )
        fechahora['iso8601'] = local.isoformat(timespec='seconds')
        fechahora['p_amd'] = local.strftime( "%Y%m%d" )
        fechahora['p_am'] = local.strftime( "%Y%m%d" )
        return fechahora

    @staticmethod
    def obtener_ruta_env(nombre_modulo:str, entorno:str) -> str:
        nombre_archivo = '.config.env'
        if entorno:
            nombre_archivo = f".{entorno.lower()}.env"
        partes = nombre_modulo.split('.')[:-1]
        ruta = Path(*partes)
        return (ruta / nombre_archivo).as_posix()

    @staticmethod
    def obtener_ruta_raiz() -> str:
        return Path('.').resolve().as_posix()

    @staticmethod
    def tipo_salida(estado:int) -> str:
        if estado < 200:
            return Constantes.SALIDA.ERROR
        if estado < 300:
            return Constantes.SALIDA.EXITO
        if estado < 400:
            return Constantes.SALIDA.AVISO
        if estado < 500:
            return Constantes.SALIDA.ALERTA
        return Constantes.SALIDA.ERROR

    @staticmethod
    def atributos_archivo(formato:str=None, tipo_mime:str=None):
        class Portador:
            def __init__(mi, formato:str, extension:str, tipo_mime:str):
                mi.formato = formato
                mi.extension = extension
                mi.tipo_mime = tipo_mime
        def _pdf():
            return Portador(Constantes.FORMATO.PDF, 'pdf', Constantes.MIME.PDF)
        def _word():
            return Portador(Constantes.FORMATO.WORD, 'docx', Constantes.MIME.DOCX)
        def _excel():
            return Portador(Constantes.FORMATO.EXCEL, 'xlsx', Constantes.MIME.XLSX)
        def _csv():
            return Portador(Constantes.FORMATO.CSV, 'csv', Constantes.MIME.CSV)
        def _html():
            return Portador(Constantes.FORMATO.HTML, 'html', Constantes.MIME.HTML)
        def _json():
            return Portador(Constantes.FORMATO.JSON, 'json', Constantes.MIME.JSON)
        def _texto():
            return Portador(Constantes.FORMATO.TEXTO, 'txt', Constantes.MIME.TXT)
        if tipo_mime:
            tipos = {
                Constantes.MIME.PDF: _pdf,
                Constantes.MIME.DOCX: _word,
                Constantes.MIME.XLSX: _excel,
                Constantes.MIME.CSV: _csv,
                Constantes.MIME.HTML: _html,
                Constantes.MIME.JSON: _json,
                Constantes.MIME.TXT: _texto,
            }
            return tipos.get(tipo_mime)()
        formatos = {
            Constantes.FORMATO.PDF: _pdf,
            Constantes.FORMATO.WORD: _word,
            Constantes.FORMATO.EXCEL: _excel,
            Constantes.FORMATO.CSV: _csv,
            Constantes.FORMATO.HTML: _html,
            Constantes.FORMATO.JSON: _json,
            Constantes.FORMATO.TEXTO: _texto,
        }
        return formatos.get(formato)()

    @staticmethod
    def crear_salida(codigo:int, tipo:str, mensaje:str='', detalles:list=[]) -> dict:
        return dict({
            'codigo': str(codigo),
            'tipo': tipo,
            'mensaje': mensaje,
            'detalles': detalles
        })


# --------------------------------------------------
# Clase: Traductor
# --------------------------------------------------
class Traductor:
    def __init__(mi, config:dict={}):
        mi.dominio:str = config.get('dominio', 'base')
        mi.dir_locales:str = config.get('dir_locales', 'locales')
        mi.zona_horaria:str = config.get('zona_horaria', '')
        mi.idiomas_disponibles:list = config.get('idiomas_disponibles', ['es'])
        mi.idioma = ''
        mi.traduccion = None

    # --------------------------------------------------
    # Métodos privados

    def _negociar_idioma(mi, idiomas_aceptados:str=None, idiomas_disponibles:list=None) -> str:
        if not idiomas_aceptados:
            idiomas_aceptados = ''
        if not idiomas_disponibles:
            idiomas_disponibles = mi.idiomas_disponibles
        mi.idiomas_disponibles = idiomas_disponibles
        idiomas = idiomas_aceptados.split(',')
        lista_idiomas = []
        for idioma in idiomas:
            partes = idioma.split(';')
            codigo = partes[0].split('-')[0].strip()
            q = 1.0
            if len(partes) > 1 and partes[1].startswith('q='):
                q = float(partes[1].split('=')[1])
            lista_idiomas.append((codigo, q))
        idiomas_ordenados = sorted(lista_idiomas, key=lambda x: x[1], reverse=True)
        idiomas_preferidos = [lang[0] for lang in idiomas_ordenados]
        for idioma_preferido in idiomas_preferidos:
            if idioma_preferido in idiomas_disponibles:
                mi.idioma = idioma_preferido
                return idioma_preferido
        mi.idioma = idiomas_disponibles[0]
        return mi.idioma

    # --------------------------------------------------
    # Métodos públicos

    def asignar_idioma(mi, idiomas_aceptados:str=None, idiomas_disponibles:list=None, dominio:str=None, dir_locales:str=None) -> str:
        mi._negociar_idioma(idiomas_aceptados, idiomas_disponibles)
        if not dominio:
            dominio = mi.dominio
        mi.dominio = dominio
        if not dir_locales:
            dir_locales = mi.dir_locales
        mi.dir_locales = dir_locales
        try:
            mi.traduccion = gettext.translation(
                domain=mi.dominio,
                localedir=mi.dir_locales,
                languages=[mi.idioma],
                fallback=False,
            )
        except Exception as e:
            raise e
        return mi.idioma

    def abrir_traduccion(mi, idiomas_aceptados:str=None, idiomas_disponibles:list=None, dominio:str=None, dir_locales:str=None) -> gettext.GNUTranslations:
        if not mi.traduccion:
            mi.asignar_idioma(
                idiomas_aceptados=idiomas_aceptados,
                idiomas_disponibles=idiomas_disponibles,
                dominio=dominio,
                dir_locales=dir_locales
            )
        return mi.traduccion.gettext

    def traducir_textos(mi, info:dict={}, claves:list=[]) -> dict:
        if info and mi.traduccion:
            seleccion = ['mensaje','error','titulo','descripcion','nombre']
            for clave, valor in info.items():
                if clave in seleccion or clave in claves:
                    info[clave] = mi.traduccion.gettext(valor)
        return info
    
    def _(mi, texto:str='') -> str:
        return  mi.traduccion.gettext(texto)


# --------------------------------------------------
# Clase estática: RegistradorLogs
# --------------------------------------------------
class RegistradorLogs:

    def __new__(cls):
        raise TypeError('Esta es una clase estática')

    @staticmethod
    def crear(nombre:str, nivel:str, archivo:str):
        from logging import (Formatter, getLogger)
        from logging.handlers import RotatingFileHandler
        registrador = getLogger(nombre)
        registrador.setLevel(nivel)
        registrador.propagate = False
        manejador = RotatingFileHandler(
            filename = archivo,
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
    def __init__(mi, mensaje:str, tipo:str='ERROR', codigo:int=500, detalles:list=[], aplicacion:str='', servicio:str='', traduccion:str='base'):
        mi.codigo = codigo
        mi.tipo = tipo
        mi.mensaje = mensaje
        mi.detalles = detalles
        mi.aplicacion = aplicacion
        mi.servicio = servicio
        mi.traduccion = traduccion
        super().__init__(mi.mensaje)

    def __str__(mi):
        return f'{mi.mensaje}'

    def __repr__(mi):
        return f'{mi.aplicacion}.{mi.servicio} | {mi.tipo} {mi.codigo}: {mi.mensaje}. {mi.detalles.__str__()}'


# --------------------------------------------------
# Clase: ErrorAutenticacion
# --------------------------------------------------
class ErrorAutenticacion(Exception):
    def __init__(mi, mensaje:str, codigo:int, url_login:str=''):
        mi.codigo = codigo
        mi.mensaje = mensaje
        mi.url_login = url_login
        super().__init__(mi.mensaje)

    def __str__(mi):
        return f'{mi.mensaje}'


# --------------------------------------------------
# Clase: ErrorDisco
# --------------------------------------------------
class ErrorDisco(Exception):
    def __init__(mi, mensaje:str, ruta:str='', codigo:int=500, detalles:list=[]):
        mi.codigo = codigo
        mi.ruta = ruta
        mi.mensaje = mensaje
        mi.detalles = detalles
        super().__init__(mi.mensaje)

    def __str__(mi):
        return f'{mi.mensaje}'

    def __repr__(mi):
        return f'{mi.codigo}: {mi.mensaje} | {mi.ruta} | {mi.detalles.__str__()}'

