# pysinergia\web.py

import time, jwt, importlib, gettext
from pathlib import Path

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Json as _Json,
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
    I_Traductor as _I_Traductor
)
from pysinergia.dominio import (
    CargaArchivo as _CargaArchivo,
)
from pysinergia.adaptadores import (
    I_Comunicador as _I_Comunicador
)
from pysinergia.conectores.disco import Disco as _Disco
from pysinergia import __version__ as api_motor

# --------------------------------------------------
# Clase: Traductor
# --------------------------------------------------
class Traductor(_I_Traductor):
    def __init__(mi, config:dict={}):
        mi.dominio:str = config.get('dominio', 'base')
        mi.dir_locales:str = config.get('dir_locales', 'locales')
        mi.zona_horaria:str = config.get('zona_horaria', 'Etc/GMT')
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
            seleccion = ['mensaje','titulo','descripcion']
            for clave, valor in info.items():
                if clave in seleccion or clave in claves:
                    info[clave] = mi.traduccion.gettext(valor)
        return info
    
    def _(mi, texto:str='') -> str:
        return  mi.traduccion.gettext(texto)

    def idioma_actual(mi) -> str:
        return mi.idioma

    def fecha_hora(mi, zona_horaria:str=None) -> dict:
        import pytz
        from datetime import datetime
        fechahora = {}
        if not zona_horaria:
            zona_horaria = mi.zona_horaria
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


# --------------------------------------------------
# Clase: Comunicador
# --------------------------------------------------
class Comunicador(_I_Comunicador):

    def __init__(mi, config_web:dict, config_disco:dict, traductor:Traductor=None):
        mi.config_web:dict = config_web or {}
        mi.idioma = None
        mi.contexto:dict = {}
        mi.disco:_Disco = mi._conectar_disco(config_disco)
        mi.traductor = traductor or Traductor()

    # --------------------------------------------------
    # Métodos privados

    def _conectar_disco(mi, config_disco:dict) -> _Disco:
        disco_fuente = config_disco.get('fuente','')
        modulo = f'pysinergia.conectores.{disco_fuente}'
        componente = getattr(importlib.import_module(modulo), config_disco.get('clase',''))
        return componente(config_disco)

    # --------------------------------------------------
    # Métodos públicos

    def procesar_peticion(mi, idiomas_aceptados:str, sesion:dict=None):
        global api_motor
        mi.idioma = mi.traductor.asignar_idioma(idiomas_aceptados=idiomas_aceptados)
        mi.contexto['sesion'] = sesion or {}
        mi.contexto['web'] = mi.config_web
        mi.contexto['web']['idioma'] = mi.idioma
        mi.contexto['web']['ruta_raiz'] = Path('.').resolve().as_posix()
        mi.contexto['web']['api_motor'] = api_motor
        mi.contexto['fecha'] = mi.traductor.fecha_hora()
        mi.contexto['peticion'] = {}

    def transformar_contenido(mi, info:dict, plantilla:str, directorio:str='.') -> str:
        from jinja2 import (Environment, FileSystemLoader)
        resultado = ''
        try:
            if Path(f'{directorio}/{plantilla}').exists():
                cargador = FileSystemLoader(directorio)
                entorno = Environment(loader=cargador)
                entorno.add_extension('jinja2.ext.i18n')
                if mi.traductor.traduccion:
                    entorno.install_gettext_translations(mi.traductor.traduccion, newstyle=True)
                template = entorno.get_template(plantilla)
                resultado = template.render(info)
            return resultado
        except Exception as e:
            raise e

    def exportar_contenido(mi, formato:str, info:dict={}, guardar:bool=False):
        try:
            modo = 't'
            opciones:dict = info['opciones']
            opciones['idioma'] = mi.idioma
            if formato == _Constantes.FORMATO.JSON:
                resultado = _Json.codificar(info)
            else:
                plantilla, ruta_plantillas = mi.comprobar_plantilla(opciones, 'plantilla')
                contenido = mi.transformar_contenido(info=info, plantilla=plantilla, directorio=ruta_plantillas)
                if formato == _Constantes.FORMATO.HTML or formato == _Constantes.FORMATO.TEXTO:
                    resultado = contenido
                else:
                    from pysinergia.adaptadores import Exportador
                    modulo = f'pysinergia.exportadores.exportador_{str(formato).lower()}'
                    clase = f'Exportador{str(formato).capitalize()}'
                    componente = getattr(importlib.import_module(modulo), clase)
                    exportador:Exportador = componente(mi.config_web)
                    resultado = exportador.generar(contenido=contenido, opciones=opciones)
                    modo = 'b'
            if guardar:
                nombre_descarga = opciones.get('nombre_descarga', '')
                carpeta_guardar = opciones.get('carpeta_guardar', '')
                ruta_archivo = str(f'{carpeta_guardar}/{nombre_descarga}').strip('/')
                mi.disco.escribir(resultado, ruta_archivo, modo)
            return resultado
        except Exception as e:
            raise e

    def obtener_nombre_descarga(mi, info:dict, extension:str='', largo:int=250, auto:bool=False) -> str:
        if 'opciones' in info:
            opciones:dict = info['opciones']
            nombre = mi.disco.normalizar_nombre(opciones.get('nombre_descarga', ''), extension, largo, auto)
            opciones['nombre_descarga'] = nombre
        else:
            nombre = mi.disco.normalizar_nombre('', extension, largo, auto)
        return nombre

    def comprobar_plantilla(mi, opciones:dict, tipo:str='') -> tuple:
        plantilla = opciones.get(tipo, '')
        ruta_plantillas = opciones.get('ruta_plantillas', None)
        if not ruta_plantillas:
            ruta = mi.config_web.get('ruta_servicio', '.')
            ruta_plantillas = f'{ruta}/plantillas'
        if plantilla:
            if not Path(f'{ruta_plantillas}/{plantilla}').exists():
                ruta_plantillas = 'backend/plantillas'
                if not Path(f'{ruta_plantillas}/{plantilla}').exists():
                    ruta_plantillas = ''
                    plantilla = ''
        opciones['ruta_plantillas'] = ruta_plantillas
        return (plantilla, ruta_plantillas)

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

    def cargar_archivo(mi, portador:_CargaArchivo, si_existe:str='RECHAZAR') -> _CargaArchivo:
        if portador and portador.es_valido:
            unico = True if si_existe == portador.RENOMBRAR else False
            portador.nombre = mi.disco.generar_nombre(portador.nombre, unico=unico)
            ruta_guardar = f'{portador.carpeta}/{portador.nombre}'
            if mi.disco.comprobar_ruta(ruta_guardar) and si_existe == portador.RECHAZAR:
                portador.es_valido = False
                portador.mensaje_error = 'El-archivo-ya-existe'
                portador.codigo = _Constantes.ESTADO._413_NO_CARGADO
                portador.resultado = _Constantes.SALIDA.ALERTA
            else:
                ruta = mi.disco.escribir(portador.contenido, ruta_guardar, modo='b')
                if not ruta:
                    portador.es_valido = False
                    portador.mensaje_error = 'Error-al-guardar-el-archivo'
                    portador.codigo = _Constantes.ESTADO._500_ERROR
                    portador.resultado = _Constantes.SALIDA.ERROR
                portador.ruta = ruta
        return portador

    def elegir_formato(mi, formato:str=None) -> str:
        if formato:
            return formato
        config_web:dict = mi.contexto.get('web')
        if config_web:
            acepta = config_web.get('acepta', '')
            if 'application/json' in acepta:
                return _Constantes.FORMATO.JSON
        return _Constantes.FORMATO.HTML

    def traspasar_traductor(mi) -> Traductor:
        if mi.traductor:
            return mi.traductor
        return None


# --------------------------------------------------
# Clase: Autenticador
# --------------------------------------------------
class Autenticador:
    def __init__(mi, config_autenticacion:dict, url_login:str=''):
        mi.secret_key = config_autenticacion.get('secret_key','')
        mi.algoritmo_jwt = config_autenticacion.get('algoritmo_jwt','')
        mi.api_keys:dict = config_autenticacion.get('api_keys','')
        mi.ruta_temp:str = config_autenticacion.get('ruta_temp','')
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
        if not id_sesion:
            id_sesion = mi.obtener_id_sesion()
        if not id_sesion:
            return {}
        archivo = f'{mi.ruta_temp}/sesiones/{id_sesion}.json'
        return _Json.leer(archivo)
    
    def guardar_sesion(mi, datos:dict) -> bool:
        id_sesion = mi.obtener_id_sesion()
        archivo = f'{mi.ruta_temp}/sesiones/{id_sesion}.json'
        return _Json.guardar(datos, archivo)


# --------------------------------------------------
# Clase: ErrorAutenticacion
# --------------------------------------------------
class ErrorAutenticacion(_ErrorPersonalizado):
    def __init__(mi, mensaje:str, codigo:int, url_login:str=''):
        mi.codigo = codigo
        mi.mensaje = mensaje
        mi.url_login = url_login
        super().__init__(mi.mensaje)

