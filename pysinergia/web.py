# pysinergia\web.py

import time, jwt, importlib, gettext, os, json
from abc import (ABC)
from pathlib import Path
from functools import lru_cache

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes,
    ErrorPersonalizado,
)
from pysinergia.dominio import (
    ArchivoCargado,
)
from pysinergia.adaptadores import (
    I_Comunicador,
    I_Traductor,
    Configuracion,
)
from pysinergia.conectores.disco import Disco
from pysinergia import (
    __nombre__ as bib_nombre,
    __version__ as bib_version,
)

# --------------------------------------------------
# Clase: Traductor
# --------------------------------------------------
class Traductor(I_Traductor):
    def __init__(mi, config:dict={}):
        mi.dominio_idioma:str = config.get('DOMINIO_IDIOMA', str(os.getenv('DOMINIO_IDIOMA')))
        mi.ruta_locales:str = config.get('RUTA_LOCALES', str(os.getenv('RUTA_LOCALES')))
        mi.idiomas_disponibles:list = config.get('IDIOMAS_DISPONIBLES', os.getenv('IDIOMAS_DISPONIBLES'))
        mi.zona_horaria:str = config.get('ZONA_HORARIA', 'UTC')
        mi.formato_fecha:str = config.get('FORMATO_FECHA', '%d/%m/%Y %H:%M')
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

    def asignar_idioma(mi, idiomas_aceptados:str=None, idiomas_disponibles:list=None, dominio_idioma:str=None, ruta_locales:str=None) -> str:
        mi._negociar_idioma(idiomas_aceptados, idiomas_disponibles)
        if not dominio_idioma:
            dominio_idioma = mi.dominio_idioma
        mi.dominio_idioma = dominio_idioma
        if not ruta_locales:
            ruta_locales = mi.ruta_locales
        mi.ruta_locales = ruta_locales
        try:
            mi.traduccion = gettext.translation(
                domain=mi.dominio_idioma,
                localedir=mi.ruta_locales,
                languages=[mi.idioma],
                fallback=False,
            )
        except Exception as e:
            raise e
        return mi.idioma

    def abrir_traduccion(mi, idiomas_aceptados:str=None, idiomas_disponibles:list=None, dominio_idioma:str=None, ruta_locales:str=None) -> gettext.GNUTranslations:
        if not mi.traduccion:
            mi.asignar_idioma(
                idiomas_aceptados=idiomas_aceptados,
                idiomas_disponibles=idiomas_disponibles,
                dominio_idioma=dominio_idioma,
                ruta_locales=ruta_locales
            )
        return mi.traduccion.gettext

    def traducir_textos(mi, info:dict={}, claves:list=[]) -> dict:
        if info and mi.traduccion:
            seleccion = ['mensaje','titulo','descripcion']
            for clave, valor in info.items():
                if clave in seleccion or clave in claves:
                    info[clave] = mi.traduccion.gettext(valor)
        return info
    
    def _(mi, texto:str='') -> str:
        return  mi.traduccion.gettext(texto)

    def idioma_actual(mi) -> str:
        return mi.idioma

    def fecha_hora(mi, fecha_hora:str=None, zona_horaria:str=None, formato_fecha:str=None) -> dict:
        import pytz
        from datetime import datetime
        try:
            zona_horaria = zona_horaria or mi.zona_horaria
            formato_fecha = formato_fecha or mi.formato_fecha
            tz = pytz.timezone(zona_horaria)
            if fecha_hora:
                fecha_dt = datetime.strptime(fecha_hora, formato_fecha)
                local = tz.localize(fecha_dt)
            else:
                local = tz.localize(datetime.now())
            diccionario = {
                'fecha': local.strftime("%d/%m/%Y"),
                'hora': local.strftime("%H:%M"),
                'hms': local.strftime("%H:%M:%S"),
                'amd': local.strftime("%Y-%m-%d"),
                'dma': local.strftime("%d-%m-%Y"),
                'mda': local.strftime("%m-%d-%Y"),
                'dm': local.strftime("%d-%m"),
                'md': local.strftime("%m-%d"),
                'ma': local.strftime("%m-%Y"),
                'am': local.strftime("%Y-%m"),
                'dia': local.strftime("%d"),
                'mes': local.strftime("%m"),
                'ano': local.strftime("%Y"),
                'amdhms': local.strftime("%Y%m%d%H%M%S"),
                'iso8601': local.isoformat(timespec='seconds'),
                'p_amd': local.strftime("%Y%m%d"),
                'p_am': local.strftime("%Y%m")
            }
            return diccionario
        except ValueError as e:
            return mi.fecha_hora()
        except pytz.UnknownTimeZoneError as e:
            print(e)
            return {}
        except Exception as e:
            print(e)
            return {}


# --------------------------------------------------
# Clase: Comunicador
# --------------------------------------------------
class Comunicador(ABC, I_Comunicador):

    def __init__(mi, config_web:dict, config_disco:dict, traductor:Traductor=None):
        mi.config_web:dict = config_web or {}
        mi.idioma = None
        mi.contexto:dict = {}
        mi.disco:Disco = mi._conectar_disco(config_disco)
        mi.traductor = traductor or Traductor()

    # --------------------------------------------------
    # Métodos privados

    def _conectar_disco(mi, config_disco:dict) -> Disco:
        try:
            fuente = config_disco.get('fuente')
            clase = config_disco.get('clase')
            componente = getattr(importlib.import_module(f'pysinergia.conectores.{fuente}'), clase)
            return componente(config_disco)
        except Exception as e:
            raise e

    def _comprobar_plantilla(mi, metadatos:dict, tipo:str='') -> tuple:
        plantilla = metadatos.get(tipo, '')
        ruta_plantillas = metadatos.get('ruta_plantillas', None)
        if not ruta_plantillas:
            ruta = mi.config_web.get('RUTA_MICROSERVICIO')
            ruta_plantillas = f'{ruta}/plantillas'
        if plantilla:
            if not Path(f'{ruta_plantillas}/{plantilla}').exists():
                ruta_plantillas = mi.config_web.get('RUTA_PLANTILLAS')
                if not Path(f'{ruta_plantillas}/{plantilla}').exists():
                    ruta_plantillas = ''
                    plantilla = ''
        metadatos['ruta_plantillas'] = ruta_plantillas
        return (plantilla, ruta_plantillas)

    # --------------------------------------------------
    # Métodos públicos

    def procesar_peticion(mi, idiomas_aceptados:str, sesion:dict=None):
        global bib_nombre, bib_version
        mi.idioma = mi.traductor.asignar_idioma(idiomas_aceptados=idiomas_aceptados)
        mi.contexto['sesion'] = sesion or {}
        mi.contexto['web'] = mi.config_web
        mi.contexto['web']['IDIOMA'] = mi.idioma
        mi.contexto['web']['API_MOTOR'] = f'{bib_nombre} v{bib_version}'
        mi.contexto['fecha'] = mi.traductor.fecha_hora()
        mi.contexto['peticion'] = {}

    def transformar_contenido(mi, info:dict, plantilla:str, ruta_plantillas:str='.') -> str:
        from jinja2 import (Environment, FileSystemLoader)
        resultado = ''
        try:
            if not Path(f'{ruta_plantillas}/{plantilla}').exists():
                ruta_plantillas = mi.config_web.get('RUTA_PLANTILLAS')
            if Path(f'{ruta_plantillas}/{plantilla}').exists():
                cargador = FileSystemLoader(ruta_plantillas)
                entorno = Environment(loader=cargador)
                entorno.add_extension('jinja2.ext.i18n')
                if mi.traductor.traduccion:
                    entorno.install_gettext_translations(mi.traductor.traduccion, newstyle=True)
                template = entorno.get_template(plantilla)
                resultado = template.render(info)
            return resultado
        except Exception as e:
            raise e

    def exportar_contenido(mi, conversion:str, info:dict={}, guardar:bool=False):
        try:
            modo = 't'
            metadatos:dict = info['metadatos']
            metadatos['idioma'] = mi.idioma
            if conversion == Constantes.CONVERSION.JSON:
                resultado = json.dumps(info, ensure_ascii=False)
            else:
                plantilla, ruta_plantillas = mi._comprobar_plantilla(metadatos, 'plantilla')
                contenido = mi.transformar_contenido(info=info, plantilla=plantilla, ruta_plantillas=ruta_plantillas)
                if conversion == Constantes.CONVERSION.HTML or conversion == Constantes.CONVERSION.TEXTO:
                    resultado = contenido
                else:
                    from pysinergia.complementos.exportador import Exportador
                    modulo = f'pysinergia.complementos.exportador_{str(conversion).lower()}'
                    clase = f'Exportador{str(conversion).capitalize()}'
                    componente = getattr(importlib.import_module(modulo), clase)
                    exportador:Exportador = componente(mi.config_web)
                    resultado = exportador.generar(contenido=contenido, opciones=metadatos)
                    modo = 'b'
            if guardar:
                nombre_descarga = metadatos.get('nombre_descarga', '')
                carpeta_guardar = metadatos.get('carpeta_guardar', '')
                ruta_archivo = str(f'{carpeta_guardar}/{nombre_descarga}').strip('/')
                mi.disco.escribir(resultado, ruta_archivo, modo)
            return resultado
        except Exception as e:
            raise e

    def generar_nombre_descarga(mi, info:dict, extension:str='', largo:int=250, auto:bool=False) -> str:
        if 'metadatos' in info:
            metadatos:dict = info['metadatos']
            nombre = mi.disco.normalizar_nombre(metadatos.get('nombre_descarga', ''), extension, largo, auto)
            metadatos['nombre_descarga'] = nombre
        else:
            nombre = mi.disco.normalizar_nombre('', extension, largo, auto)
        return nombre

    def transferir_contexto(mi, datos:dict=None) -> dict:
        if mi.contexto.get('datos', None) is None:
            mi.contexto['datos'] = {}
        if datos is not None:
            for clave, valor in datos.items():
                mi.contexto['datos'][clave] = valor
        return mi.contexto

    def generar_encabezados(mi, tipo_mime:str, charset:str='', disposicion:str='inline', nombre_descarga:str='') -> dict:
        content_type = f"{tipo_mime}; charset={charset}" if charset else tipo_mime
        encabezados = {'Content-Type': content_type}
        if nombre_descarga:
            encabezados['Content-disposition'] = f'{disposicion}; filename="{nombre_descarga}"'
        else:
            encabezados['Content-disposition'] = disposicion
        return encabezados

    def cargar_archivo(mi, portador:ArchivoCargado, si_existe:str='RECHAZAR') -> ArchivoCargado:
        if portador and portador.es_valido:
            unico = True if si_existe == portador.RENOMBRAR else False
            portador.nombre = mi.disco.generar_nombre(portador.nombre, unico=unico)
            ruta_guardar = f'{portador.carpeta}/{portador.nombre}'
            if mi.disco.comprobar_ruta(ruta_guardar) and si_existe == portador.RECHAZAR:
                portador.es_valido = False
                portador.mensaje_error = 'El-archivo-ya-existe'
                portador.codigo = Constantes.ESTADO._413_NO_CARGADO
                portador.conclusion = Constantes.CONCLUSION.ALERTA
            else:
                ruta = mi.disco.escribir(portador.contenido, ruta_guardar, modo='b')
                if not ruta:
                    portador.es_valido = False
                    portador.mensaje_error = 'Error-al-guardar-el-archivo'
                    portador.codigo = Constantes.ESTADO._500_ERROR
                    portador.conclusion = Constantes.CONCLUSION.ERROR
                portador.ruta = ruta
        return portador

    def elegir_conversion(mi, conversion:str=None) -> str:
        if conversion:
            return conversion
        config_web:dict = mi.contexto.get('web')
        if config_web:
            acepta = config_web.get('ACEPTA', '')
            if 'application/json' in acepta:
                return Constantes.CONVERSION.JSON
        return Constantes.CONVERSION.HTML

    def traspasar_traductor(mi) -> Traductor:
        if mi.traductor:
            return mi.traductor
        return None


# --------------------------------------------------
# Clase: Autenticador
# --------------------------------------------------
class Autenticador(ABC):
    def __init__(mi, config_autenticacion:dict, url_login:str=''):
        mi.secret_key = config_autenticacion.get('SECRET_KEY')
        mi.algoritmo_jwt = config_autenticacion.get('ALGORITMO_JWT')
        mi.api_keys:dict = config_autenticacion.get('API_KEYS')
        mi.ruta_temp:str = config_autenticacion.get('RUTA_TEMP')
        mi.url_login:str = url_login
        mi.token:str = None

    # --------------------------------------------------
    # Métodos privados

    def _verificar_jwt(mi) -> bool:
        es_valido:bool = False
        try:
            payload = mi._decodificar_jwt()
        except:
            payload = None
        if payload:
            es_valido = True
        return es_valido

    def _decodificar_jwt(mi) -> dict:
        if not mi.token:
            return None
        try:
            token_decodificado = jwt.decode(mi.token, mi.secret_key, algorithms=[mi.algoritmo_jwt])
            return token_decodificado if token_decodificado['caducidad'] >= time.time() else None
        except:
            return {}

    # --------------------------------------------------
    # Métodos públicos

    def obtener_id_sesion(mi) -> str:
        token_decodificado = mi._decodificar_jwt()
        if token_decodificado:
            return token_decodificado.get('id_sesion')
        return ''

    def firmar_token(mi, id_sesion:str, duracion:int=30) -> str:
        payload = {
            'id_sesion': id_sesion,
            'caducidad': time.time() + 60 * duracion
        }
        mi.token = jwt.encode(payload, mi.secret_key, algorithm=mi.algoritmo_jwt)
        return mi.token

    def recuperar_sesion(mi, id_sesion:str='') -> dict:
        sesion = {}
        if not id_sesion:
            id_sesion = mi.obtener_id_sesion()
        if not id_sesion:
            return sesion
        archivo = f'{mi.ruta_temp}/sesiones/{id_sesion}.json'
        if Path(archivo).is_file():
            with open(archivo, 'r', encoding='utf-8') as f:
                sesion = json.load(f)
        return sesion
    
    def guardar_sesion(mi, datos:dict) -> bool:
        id_sesion = mi.obtener_id_sesion()
        archivo = f'{mi.ruta_temp}/sesiones/{id_sesion}.json'
        if datos:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        return False


# --------------------------------------------------
# Clase: ErrorAutenticacion
# --------------------------------------------------
class ErrorAutenticacion(ErrorPersonalizado):
    def __init__(mi, mensaje:str, codigo:int, url_login:str=''):
        super().__init__(
            mensaje=mensaje,
            codigo=codigo,
            nivel_registro=Constantes.REGISTRO.INFO
        )
        mi.url_login = url_login


# --------------------------------------------------
# Funcion: configurar_microservicio
# --------------------------------------------------
@lru_cache
def configurar_microservicio(modelo_base:Configuracion, ruta_origen:str, env_aplicacion:str=None, entorno:str=None) -> Configuracion:
    from dotenv import dotenv_values
    prefijo_entorno = f'{entorno.lower()}' if entorno else 'config'
    ruta_microservicio_path = Path(ruta_origen).parent
    lista_env:list[Path] = [(ruta_microservicio_path / f'.{prefijo_entorno}.env')]
    if env_aplicacion:
        lista_env.append((ruta_microservicio_path.parent / f'_config/.{prefijo_entorno}.{env_aplicacion}.env'))
    valores_configuracion = {
        'RUTA_MICROSERVICIO': ruta_microservicio_path.as_posix(),
        'MICROSERVICIO': ruta_microservicio_path.name,
    }
    for archivo in lista_env:
        if archivo.exists():
            valores_configuracion.update(dotenv_values(archivo))
    configuracion:Configuracion = modelo_base(**valores_configuracion)
    configuracion.iniciar()
    return configuracion


# --------------------------------------------------
# Funcion: configurar_servidor_api
# --------------------------------------------------
def configurar_servidor_api(ruta_origen:str, archivo_env:str):
    from dotenv import dotenv_values
    try:
        archivo_env_path = Path(archivo_env)
        claves = dotenv_values(archivo_env_path)
        for clave, valor in claves.items():
            os.environ[clave] = valor
        ruta_lib_ffmpeg = Path(os.getenv('RUTA_LIB_FFMPEG','')).resolve()
        if ruta_lib_ffmpeg.is_dir():
            os.environ['PATH'] = str(ruta_lib_ffmpeg) + os.pathsep + os.getenv('PATH')
        if os.getenv('FRAMEWORK') == 'flask':
            from pysinergia.interfaces.web_flask import ServidorApi
        elif os.getenv('FRAMEWORK') == 'fastapi':
            from pysinergia.interfaces.web_fastapi import ServidorApi
        return ServidorApi(ruta_origen)
    except Exception as e:
        raise e

