# pysinergia\web.py

import time, jwt, importlib
from pathlib import Path

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Json as _Json,
    Constantes as _Constantes,
    Funciones as _Funciones,
)
from pysinergia.dominio import (
    CargaArchivo as _CargaArchivo,
)
from pysinergia.adaptadores import (
    I_ConectorDisco as _I_Disco,
    I_Comunicador as _I_Comunicador
)
from pysinergia import __version__ as api_motor

# --------------------------------------------------
# Clase: Comunicador
# --------------------------------------------------
class Comunicador(_I_Comunicador):

    def __init__(mi, config_web:dict, config_disco:dict):
        mi.config_web:dict = config_web or {}
        mi.idioma = None
        mi.traductor = None
        mi.contexto:dict = {}
        mi.disco:_I_Disco = mi._conectar_disco(config_disco)

    # --------------------------------------------------
    # Métodos privados

    def _conectar_disco(mi, config_disco:dict) -> _I_Disco:
        disco_fuente = config_disco.get('fuente','')
        modulo = f'pysinergia.conectores.{disco_fuente}'
        componente = getattr(importlib.import_module(modulo), config_disco.get('clase',''))
        return componente(config_disco)

    def _asignar_idioma(mi, idiomas_aceptados:str):
        import gettext
        mi.idioma = negociar_idioma(idiomas_aceptados, mi.config_web.get('idiomas'))
        try:
            mi.traductor = gettext.translation(
                domain=mi.config_web.get('traduccion'),
                localedir=mi.config_web.get('dir_locales'),
                languages=[mi.idioma],
                fallback=False,
            )
        except Exception as e:
            raise e

    # --------------------------------------------------
    # Métodos públicos

    def procesar_peticion(mi, idiomas_aceptados:str, sesion:dict=None):
        global api_motor
        mi._asignar_idioma(idiomas_aceptados)
        mi.contexto['sesion'] = sesion or {}
        mi.contexto['web'] = mi.config_web
        mi.contexto['web']['idioma'] = mi.idioma
        mi.contexto['web']['api_motor'] = api_motor
        mi.contexto['web']['ruta_raiz'] = _Funciones.obtener_ruta_raiz()
        mi.contexto['fecha'] = _Funciones.fecha_hora(zona_horaria=mi.config_web.get('zona_horaria'))
        mi.contexto['peticion'] = {}

    def transformar_contenido(mi, info:dict, plantilla:str, directorio:str='.') -> str:
        from jinja2 import (Environment, FileSystemLoader)
        resultado = ''
        try:
            if Path(f'{directorio}/{plantilla}').exists():
                cargador = FileSystemLoader(directorio)
                entorno = Environment(loader=cargador)
                entorno.add_extension('jinja2.ext.i18n')
                if mi.traductor:
                    entorno.install_gettext_translations(mi.traductor, newstyle=True)
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
            if formato == _Constantes.FORMATO.JSON or formato == _Constantes.FORMATO.TEXTO:
                resultado = _Json.codificar(info)
            else:
                plantilla, ruta_plantillas = mi.comprobar_plantilla(opciones, 'plantilla')
                contenido = mi.transformar_contenido(info=info, plantilla=plantilla, directorio=ruta_plantillas)
                if formato == _Constantes.FORMATO.HTML:
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
                nombre_archivo = opciones.get('nombre_archivo', '')
                carpeta_guardar = opciones.get('carpeta_guardar', '')
                ruta_archivo = str(f'{carpeta_guardar}/{nombre_archivo}').strip('/')
                mi.disco.escribir(resultado, ruta_archivo, modo)
            return resultado
        except Exception as e:
            raise e

    def obtener_nombre_archivo(mi, info:dict, extension:str='', largo:int=250, auto:bool=False) -> str:
        if 'opciones' in info:
            opciones:dict = info['opciones']
            nombre = mi.disco.normalizar_nombre(opciones.get('nombre_archivo', ''), extension, largo, auto)
            opciones['nombre_archivo'] = nombre
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

    def transferir_contexto(mi) -> dict:
        return mi.contexto

    def generar_encabezados(mi, tipo_mime:str, charset:str='', disposicion:str='inline', nombre_archivo:str='') -> dict:
        content_type = f"{tipo_mime}; charset={charset}" if charset else tipo_mime
        encabezados = {'Content-Type': content_type}
        if nombre_archivo:
            encabezados['Content-disposition'] = f'{disposicion}; filename="{nombre_archivo}"'
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
            else:
                ruta = mi.disco.escribir(portador.contenido, ruta_guardar, modo='b')
                if not ruta:
                    portador.es_valido = False
                    portador.mensaje_error = 'Error-al-guardar-el-archivo'
                portador.ruta = ruta
        return portador

    def determinar_formato(mi, formato:str=None) -> str:
        if formato:
            return formato
        config_web:dict = mi.contexto.get('web')
        if config_web:
            acepta = config_web.get('acepta', '')
            if 'application/json' in acepta:
                return _Constantes.FORMATO.JSON
        return _Constantes.FORMATO.HTML

    # --------------------------------------------------

    def traspasar_traductor(mi):
        if mi.traductor:
            return mi.traductor.gettext
        return None

    def traducir_textos(mi, info:dict={}) -> dict:
        if info:
            seleccion = ['mensaje','error','titulo','descripcion','nombre']
            for clave, valor in info.items():
                if clave in seleccion:
                    info[clave] = mi.traductor.gettext(valor)
        return info


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
# Funcion: negociar_idioma
# --------------------------------------------------
def negociar_idioma(idiomas_aceptados:str, idiomas_disponibles:list) -> str:
    if not idiomas_aceptados:
        idiomas_aceptados = ''
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
            return idioma_preferido
    return idiomas_disponibles[0]

