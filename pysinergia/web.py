# pysinergia\web.py

import time, jwt

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Funciones as _F,
    Json as _Json,
)

# --------------------------------------------------
# Clase: Comunicador
# --------------------------------------------------
class Comunicador:
    def __init__(mi, config:dict):
        mi.config:dict = config
        mi.idioma = None
        mi.traductor = None

    # --------------------------------------------------
    # Métodos públicos

    def asignar_idioma(mi, idiomas_aceptados:str):
        import gettext
        mi.idioma = _F.negociar_idioma(idiomas_aceptados, mi.config.get('idiomas'))
        mi.traductor = gettext.translation(
            domain=mi.config.get('traduccion'),
            localedir=mi.config.get('dir_locales'),
            languages=[mi.idioma],
            fallback=False,
        )

    def transformar_contenido(mi, info:dict, plantilla:str, directorio:str='./') -> str:
        from jinja2 import (Environment, FileSystemLoader)
        import os
        resultado = ''
        if os.path.exists(f'{directorio}/{plantilla}'):
            cargador = FileSystemLoader(directorio)
            entorno = Environment(loader=cargador)
            entorno.add_extension('jinja2.ext.i18n')
            if mi.traductor:
                entorno.install_gettext_translations(mi.traductor, newstyle=True)
            template = entorno.get_template(plantilla)
            resultado = template.render(info)
        return resultado

    def exportar_info(mi, formato:str, info:dict={}):
        import importlib
        from pysinergia.adaptadores import I_Exportador
        info['opciones']['idioma'] = mi.idioma
        plantilla = info['opciones'].get('plantilla')
        contenido = mi.transformar_contenido(info=info, plantilla=plantilla)
        modulo = f'pysinergia.exportadores.exportador_{str(formato).lower()}'
        clase = f'Exportador{str(formato).capitalize()}'
        componente = getattr(importlib.import_module(modulo), clase)
        exportador:I_Exportador = componente(mi.config)
        return exportador.generar(contenido=contenido, opciones=info['opciones'])


# --------------------------------------------------
# Clase: Autenticador
# --------------------------------------------------
class Autenticador:
    def __init__(mi, secreto:str, algoritmo:str='HS256', url_login:str='', api_keys:dict={}, ruta_temp:str=''):
        mi.secreto = secreto
        mi.algoritmo = algoritmo
        mi.url_login:str = url_login
        mi.api_keys:dict = api_keys
        mi.ruta_temp:str = ruta_temp
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
            token_decodificado = jwt.decode(mi.token, mi.secreto, algorithms=[mi.algoritmo])
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
        mi.token = jwt.encode(payload, mi.secreto, algorithm=mi.algoritmo)
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
