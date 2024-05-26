# pysinergia\web.py

import time, jwt

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Json as _Json,
    Constantes as _Constantes,
)
from pysinergia.adaptadores import I_ConectorDisco as _Disco

# --------------------------------------------------
# Clase: Comunicador
# --------------------------------------------------
class Comunicador:
    def __init__(mi, config:dict, disco:_Disco):
        mi.config:dict = config or {}
        mi.disco:_Disco = disco
        mi.idioma = None
        mi.traductor = None
        mi.contexto:dict = {}

    # --------------------------------------------------
    # Métodos públicos

    def asignar_idioma(mi, idiomas_aceptados:str):
        import gettext
        mi.idioma = negociar_idioma(idiomas_aceptados, mi.config.get('idiomas'))
        try:
            mi.traductor = gettext.translation(
                domain=mi.config.get('traduccion'),
                localedir=mi.config.get('dir_locales'),
                languages=[mi.idioma],
                fallback=False,
            )
        except Exception as e:
            raise e

    def transformar_contenido(mi, info:dict, plantilla:str, directorio:str='.') -> str:
        from jinja2 import (Environment, FileSystemLoader)
        import os
        resultado = ''
        try:
            if os.path.exists(f'{directorio}/{plantilla}'):
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
                    import importlib
                    from pysinergia.adaptadores import Exportador
                    modulo = f'pysinergia.exportadores.exportador_{str(formato).lower()}'
                    clase = f'Exportador{str(formato).capitalize()}'
                    componente = getattr(importlib.import_module(modulo), clase)
                    exportador:Exportador = componente(mi.config)
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
        import os
        plantilla = opciones.get(tipo, '')
        ruta_plantillas = opciones.get('ruta_plantillas', None)
        if not ruta_plantillas:
            ruta = mi.config.get('ruta_servicio', '.')
            ruta_plantillas = f'{ruta}/plantillas'
        if plantilla:
            if not os.path.exists(f'{ruta_plantillas}/{plantilla}'):
                ruta_plantillas = 'backend/plantillas'
                if not os.path.exists(f'{ruta_plantillas}/{plantilla}'):
                    ruta_plantillas = ''
                    plantilla = ''
        opciones['ruta_plantillas'] = ruta_plantillas
        return plantilla, ruta_plantillas

    def traspasar_contexto(mi) -> dict:
        return mi.contexto


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

