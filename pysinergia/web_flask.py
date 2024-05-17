# pysinergia\web_flask.py

from typing import Dict
from functools import wraps
import time, jwt, os

# --------------------------------------------------
# Importaciones de Infraestructura Web

from flask import (
    Flask,
    Response,
    request,
    redirect,
    send_from_directory,
)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes as _C,
    Funciones as _F,
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
            return send_from_directory(mi.dir_frontend, 'favicon.ico')

    def _configurar_cors(mi, api:Flask, origenes_cors:list):
        from flask_cors import CORS
        CORS(api, resources={
                r'/*': {
                    'origins': origenes_cors,
                    'methods': ['GET','POST','PUT','DELETE']
                }
            }
        )

    def _obtener_url(mi) -> str:
        url = f'{request.url}'
        return f'{request.method} {url}'

    # --------------------------------------------------
    # Métodos públicos

    def crear_api(mi, dir_frontend:str, alias_frontend:str, origenes_cors:list=['*'], titulo:str='', descripcion:str='', version:str='', doc:bool=False) -> Flask:
        mi.dir_frontend = os.path.abspath(dir_frontend)
        api = Flask(__name__,
            static_url_path=f'/{alias_frontend}',
            static_folder=mi.dir_frontend,
        )
        mi.titulo = titulo
        mi.descripcion = descripcion
        mi.version = version
        mi._configurar_cors(api, origenes_cors)
        mi._configurar_encabezados(api)
        mi._configurar_endpoints(api)
        api.app_context().push()
        return api

    def mapear_enrutadores(mi, api:Flask, ubicacion:str):
        import importlib
        servicios = os.listdir(ubicacion)
        modulo_base = 'web_flask'
        for servicio in servicios:
            try:
                enrutador = importlib.import_module(f'{ubicacion}.{servicio}.{modulo_base}')
                api.register_blueprint(getattr(enrutador, 'enrutador'))
            except Exception as e:
                print(e)
                continue

    def iniciar_servicio(mi, app:Flask, host:str, puerto:int, entorno:str):
        if entorno == _C.ENTORNO.DESARROLLO or entorno == _C.ENTORNO.LOCAL:
            ssl_cert=os.path.join(os.path.abspath('.'), 'cert.pem')
            ssl_key=os.path.join(os.path.abspath('.'), 'key.pem')
            app.run(
                host=host,
                port=puerto,
                ssl_context=(ssl_cert, ssl_key),
            )

    def manejar_errores(mi, api:Flask, registro_logs:str):
        from werkzeug.exceptions import (
            HTTPException,
            InternalServerError,
        )
        from pydantic import ValidationError

        @api.errorhandler(_ErrorPersonalizado)
        def _error_personalizado_handler(exc:_ErrorPersonalizado):
            salida = _F.crear_salida(
                codigo=exc.codigo,
                tipo=exc.tipo,
                mensaje=exc.mensaje,
                detalles=exc.detalles
            )
            if exc.tipo == _C.SALIDA.ERROR:
                nombre = registro_logs
                if exc.aplicacion and exc.servicio:
                    nombre = f'{exc.aplicacion}_{exc.servicio}'
                _RegistradorLogs.crear(f'{nombre}', 'ERROR', f'./logs/{nombre}.log').error(
                    f'{mi._obtener_url()} | {salida.__repr__()}'
                )
            return Response(
                _Json.codificar(salida),
                status=exc.codigo,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(_ErrorAutenticacion)
        def _error_autenticacion_handler(exc:_ErrorAutenticacion):
            salida = _F.crear_salida(
                codigo=exc.codigo,
                tipo=_C.SALIDA.ALERTA,
                mensaje=exc.mensaje,
                detalles=[]
            )
            if exc.url_login:
                return redirect(exc.url_login)
            return Response(
                _Json.codificar(salida),
                status=exc.codigo,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(ValidationError)
        def _error_validation_handler(exc:ValidationError):
            errores = exc.errors()
            detalles = []
            for error in errores:
                detalles.append({
                    'error': error['msg'],
                    'origen': error['loc'],
                    'valor': error['input']
                })
            salida = _F.crear_salida(
                codigo=_C.ESTADO.HTTP_422_NO_PROCESABLE,
                tipo=_C.SALIDA.ALERTA,
                mensaje='Los datos recibidos no fueron procesados correctamente',
                detalles=detalles
            )
            return Response(
                _Json.codificar(salida),
                status=_C.ESTADO.HTTP_422_NO_PROCESABLE,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(HTTPException)
        def _error_http_handler(exc:HTTPException):
            salida = _F.crear_salida(
                codigo=exc.code,
                tipo=_F.tipo_salida(exc.code),
                mensaje=exc.description
            )
            if exc.code >= 500:
                _RegistradorLogs.crear(registro_logs, 'ERROR', f'./logs/{registro_logs}.log').error(
                    f'{mi._obtener_url()} | {salida.__repr__()}'
                )
            return Response(
                _Json.codificar(salida),
                status=exc.code,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(InternalServerError)
        def _error_internal_handler(exc:InternalServerError):
            descripcion = ''
            origen = exc.original_exception
            if origen.__doc__:
                descripcion = origen.__doc__
            if len(origen.args) > 0:
                descripcion = origen.args[0]
            salida = _F.crear_salida(
                codigo=_C.ESTADO.HTTP_500_ERROR,
                tipo=_F.tipo_salida(_C.ESTADO.HTTP_500_ERROR),
                mensaje=descripcion
            )
            _RegistradorLogs.crear(registro_logs, 'ERROR', f'./logs/{registro_logs}.log').error(
                f'{mi._obtener_url()} | {salida.__repr__()}'
            )
            return Response(
                _Json.codificar(salida),
                status=_C.ESTADO.HTTP_500_ERROR,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(Exception)
        def _unhandled_errorhandler(exc:Exception):
            import sys
            exception_type, exception_value, exception_traceback = sys.exc_info()
            exception_name = getattr(exception_type, '__name__', None)
            mensaje = f'Error interno del Servidor <{exception_name}: {exception_value}>'
            salida = _F.crear_salida(
                codigo=_C.ESTADO.HTTP_500_ERROR,
                tipo=_C.SALIDA.ERROR,
                mensaje=mensaje
            )
            _RegistradorLogs.crear(registro_logs, 'ERROR', f'./logs/{registro_logs}.log').error(
                f'{mi._obtener_url()} | {mensaje}'
            )
            return Response(
                _Json.codificar(salida),
                status=_C.ESTADO.HTTP_500_ERROR,
                mimetype=_C.MIME.JSON
            )


# --------------------------------------------------
# Clase: ComunicadorWeb
# --------------------------------------------------
class ComunicadorWeb:
    def __init__(mi):
        ...

    # --------------------------------------------------
    # Métodos públicos

    def transformar_contenido(mi, info:dict, plantilla:str, directorio:str='./') -> str:
        from jinja2 import (Environment, FileSystemLoader)
        resultado = ''
        if os.path.exists(f'{directorio}/{plantilla}'):
            cargador = FileSystemLoader(directorio)
            entorno = Environment(loader=cargador)
            template = entorno.get_template(plantilla)
            resultado = template.render(info)
            resultado = resultado.replace('{ruta_raiz}', _F.obtener_ruta_raiz())
        return resultado

    def generar_documento_pdf(mi, nombre_archivo:str, estilos_css:str, plantilla_html:str, info:dict={}):
        from weasyprint import HTML, CSS
        import io
        encabezados = {
            'Content-Type': _C.MIME.PDF,
            'Content-disposition': f'inline; filename={nombre_archivo}'
        }
        contenido = mi.transformar_contenido(info=info, plantilla=plantilla_html)
        css = CSS(filename=estilos_css)
        pdf = HTML(string=contenido).write_pdf(stylesheets=[css])
        return Response(io.BytesIO(pdf), headers=encabezados)


# --------------------------------------------------
# Clase: AutenticadorWeb
# --------------------------------------------------
class AutenticadorWeb:
    def __init__(mi, secreto:str, algoritmo:str='HS256', url_login:str='', api_keys:dict={}, ruta_temp:str='tmp'):
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

    def _validar_apikey(mi) -> str:
        mensaje = 'API key no válida'
        if 'Authorization' in request.headers:
            api_key_header = request.headers.get('Authorization').replace('Bearer ', '')
            if mi.api_keys and api_key_header and api_key_header in mi.api_keys:
                return mi.api_keys.get(api_key_header)
        raise _ErrorAutenticacion(
            mensaje=mensaje,
            codigo=_C.ESTADO.HTTP_403_NO_AUTORIZADO,
        )
    
    def _validar_token(mi) -> str:
        mensaje = 'Encabezado de autorización no válido.'
        if 'X-Token' in request.headers:
            sesion_token_header = request.headers.get('X-Token')
            if sesion_token_header:
                mi.token = sesion_token_header
                if not mi._verificar_jwt():
                    mensaje = 'Token no válido o caducado.'
                else:
                    return mi.token
        raise _ErrorAutenticacion(
            mensaje=mensaje,
            codigo=_C.ESTADO.HTTP_401_NO_AUTENTICADO,
            url_login=mi.url_login
        )

    # --------------------------------------------------
    # Métodos públicos

    def obtener_id_sesion(mi):
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

    def validar_todo(mi, f):
        @wraps(f)
        def decorador(*args, **kwargs):
            mi._validar_apikey()
            mi._validar_token()
            return f(*args, **kwargs)
        return decorador

    def validar_token(mi, f):
        @wraps(f)
        def decorador(*args, **kwargs):
            mi._validar_token()
            return f(*args, **kwargs)
        return decorador

    def validar_apikey(mi, f):
        @wraps(f)
        def decorador(*args, **kwargs):
            mi._validar_apikey()
            return f(*args, **kwargs)
        return decorador

    def recuperar_sesion(mi, aplicacion:str, id_sesion:str='') -> Dict:
        if not id_sesion:
            id_sesion = mi.obtener_id_sesion()
        archivo = f'{mi.ruta_temp}/{aplicacion}/sesiones/{id_sesion}.json'
        return _Json.leer(archivo)
    
    def guardar_sesion(mi, aplicacion:str, datos:dict) -> bool:
        id_sesion = mi.obtener_id_sesion()
        archivo = f'{mi.ruta_temp}/{aplicacion}/sesiones/{id_sesion}.json'
        return _Json.guardar(datos, archivo)

