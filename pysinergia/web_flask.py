# pysinergia\web_flask.py

from typing import Dict
import time, jwt, os

# --------------------------------------------------
# Importaciones de Infraestructura Web

from flask import (
    Flask,
    Response,
    request,
    make_response,
    redirect,
)
from flask_cors import CORS
from jinja2 import (
    Environment,
    FileSystemLoader,
)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes as _Constantes,
    Funciones as _Funciones,
    Json as _Json,
    ErrorPersonalizado as _ErrorPersonalizado,
    ErrorAutenticacion as _ErrorAutenticacion,
    RegistradorLogs as _RegistradorLogs,
)
from pysinergia import __version__ as api_motor

# --------------------------------------------------
# Clase: ServidorApi
# --------------------------------------------------
class ServidorApi:

    # --------------------------------------------------
    # Métodos privados

    def _configurar_encabezados(mi, api:Flask):
        @api.after_request
        def procesar_salidas(respuesta:Response):
            respuesta.headers['X-API-Motor'] = f"{api_motor}"
            return respuesta

    def _configurar_endpoints(mi, api:Flask):

        @api.route('/', methods=['GET'])
        def entrypoint():
            return {'api-entrypoint': f'{api_motor}'}

        @api.route('/favicon.ico', methods=['GET'])
        def favicon():
            return ''

    def _configurar_cors(mi, api:Flask, origenes_cors:list):
        CORS(api, resources={
                r'/*': {
                    'origins': origenes_cors,
                    'methods': ['GET','POST','PUT','DELETE']
                }
            }
        )

    def _crear_salida(mi, codigo:int, tipo:str, mensaje:str='', detalles:list=[]) -> dict:
        return dict({
            'codigo': str(codigo),
            'tipo': tipo,
            'mensaje': mensaje,
            'detalles': detalles
        })

    def _tipo_salida(mi, estado:int) -> str:
        if estado < 200:
            return _Constantes.SALIDA.ERROR
        if estado < 300:
            return _Constantes.SALIDA.EXITO
        if estado < 400:
            return _Constantes.SALIDA.AVISO
        if estado < 500:
            return _Constantes.SALIDA.ALERTA
        return _Constantes.SALIDA.ERROR

    def _obtener_url(mi) -> str:
        url = f'{request.url}'
        return f'{request.method} {url}'

    # --------------------------------------------------
    # Métodos públicos

    def crear_api(mi, titulo:str='', descripcion:str='', version:str='', origenes_cors:list=['*'], doc:bool=False) -> Flask:
        api = Flask(__name__)
        mi.titulo = titulo
        mi.descripcion = descripcion
        mi.version = version
        mi._configurar_cors(api, origenes_cors)
        mi._configurar_encabezados(api)
        mi._configurar_endpoints(api)
        api.app_context().push()
        api.test_request_context().push()
        return api

    def asignar_frontend(mi, api:Flask, directorio:str, alias:str):
        api.static_folder = directorio
        api.static_url_path = f'/{alias}'

    def mapear_enrutadores(mi, api:Flask, ubicacion:str):
        import importlib
        servicios = os.listdir(ubicacion)
        modulo_base = 'web_flask'
        for servicio in servicios:
            try:
                ruta_modulo = os.path.join(ubicacion, servicio, f'{modulo_base}.py')
                if os.path.isfile(ruta_modulo):
                    enrutador = importlib.import_module(f'{ubicacion}.{servicio}.{modulo_base}')
                    api.register_blueprint(getattr(enrutador, 'enrutador'))
            except Exception as e:
                print(e)
                continue

    def iniciar_servicio(mi, app:str, host:str, puerto:int):
        import uvicorn
        uvicorn.run(
            app,
            host=host,
            port=puerto,
            ssl_keyfile='./key.pem',
            ssl_certfile='./cert.pem',
            reload=True
        )

    def manejar_errores(mi, api:Flask, registro_logs:str):
        from werkzeug.exceptions import HTTPException, InternalServerError

        @api.errorhandler(_ErrorPersonalizado)
        def _error_personalizado_handler(exc:_ErrorPersonalizado):
            salida = mi._crear_salida(
                codigo=exc.codigo,
                tipo=exc.tipo,
                mensaje=exc.mensaje,
                detalles=exc.detalles
            )
            if exc.tipo == _Constantes.SALIDA.ERROR:
                nombre = registro_logs
                if exc.aplicacion and exc.servicio:
                    nombre = f'{exc.aplicacion}_{exc.servicio}'
                _RegistradorLogs.crear(f'{nombre}', 'ERROR', f'./logs/{nombre}.log').error(
                    f'{mi._obtener_url()} | {salida.__repr__()}'
                )
            return make_response(_Json.codificar(salida), exc.codigo)

        @api.errorhandler(_ErrorAutenticacion)
        def _error_autenticacion_handler(exc:_ErrorAutenticacion):
            salida = mi._crear_salida(
                codigo=exc.codigo,
                tipo=_Constantes.SALIDA.ALERTA,
                mensaje=exc.mensaje,
                detalles=[]
            )
            if exc.url_login:
                return redirect(exc.url_login)
            return make_response(_Json.codificar(salida), exc.codigo)

        @api.errorhandler(HTTPException)
        def _error_http_handler(exc:HTTPException):
            salida = mi._crear_salida(
                codigo=exc.code,
                tipo=mi._tipo_salida(exc.code),
                mensaje=exc.description
            )
            if exc.code >= 500:
                _RegistradorLogs.crear(registro_logs, 'ERROR', f'./logs/{registro_logs}.log').error(
                    f'{mi._obtener_url()} | {salida.__repr__()}'
                )
            return make_response(_Json.codificar(salida), exc.code)

        @api.errorhandler(InternalServerError)
        def _error_internal_handler(exc:InternalServerError):
            descripcion = ''
            origen = exc.original_exception
            if origen.__doc__:
                descripcion = origen.__doc__
            if len(origen.args) > 0:
                descripcion = origen.args[0]
            salida = mi._crear_salida(
                codigo=500,
                tipo=mi._tipo_salida(500),
                mensaje=descripcion
            )
            _RegistradorLogs.crear(registro_logs, 'ERROR', f'./logs/{registro_logs}.log').error(
                f'{mi._obtener_url()} | {salida.__repr__()}'
            )
            return make_response(_Json.codificar(salida), 500)

        @api.errorhandler(Exception)
        def _unhandled_errorhandler(exc:Exception):
            import sys
            exception_type, exception_value, exception_traceback = sys.exc_info()
            exception_name = getattr(exception_type, '__name__', None)
            mensaje = f'Error interno del Servidor <{exception_name}: {exception_value}>'
            salida = mi._crear_salida(
                codigo=500,
                tipo=_Constantes.SALIDA.ERROR,
                mensaje=mensaje
            )
            _RegistradorLogs.crear(registro_logs, 'ERROR', f'./logs/{registro_logs}.log').error(
                f'{mi._obtener_url()} | {mensaje}'
            )
            return salida


# --------------------------------------------------
# Clase: ComunicadorWeb
# --------------------------------------------------
class ComunicadorWeb():
    def __init__(mi, ruta_temp:str='tmp'):
        mi.ruta_temp:str = ruta_temp

    # --------------------------------------------------
    # Métodos públicos

    def recuperar_sesion(mi, id_sesion:str, aplicacion:str) -> Dict:
        archivo = f'{mi.ruta_temp}/{aplicacion}/sesiones/{id_sesion}.json'
        return _Json.leer(archivo)
    
    def guardar_sesion(mi, id_sesion:str, aplicacion:str, datos:dict) -> bool:
        archivo = f'{mi.ruta_temp}/{aplicacion}/sesiones/{id_sesion}.json'
        return _Json.guardar(datos, archivo)

    def transformar_contenido(mi, info:dict, plantilla:str, directorio:str='./') -> str:
        resultado = ''
        if os.path.exists(f'{directorio}/{plantilla}'):
            cargador = FileSystemLoader(directorio)
            entorno = Environment(loader=cargador)
            template = entorno.get_template(plantilla)
            resultado = template.render(info)
            resultado = resultado.replace('{ruta_raiz}', _Funciones.obtener_ruta_raiz())
        return resultado


# --------------------------------------------------
# Clase: AutenticadorWeb
# --------------------------------------------------
class AutenticadorWeb():
    def __init__(mi, secreto:str, algoritmo:str='HS256', url_login:str=None, api_keys:dict={}):
        mi.secreto = secreto
        mi.algoritmo = algoritmo
        mi.url_login:str = url_login
        mi.api_keys:dict = api_keys
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

    def id_sesion(mi):
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

    def validar_apikey(mi, api_key_header:str) -> str:
        if mi.api_keys:
            if api_key_header in mi.api_keys:
                return mi.api_keys.get(api_key_header)
            raise _ErrorAutenticacion(
                codigo=401,
                mensaje='API key no válida'
            )
        return None

