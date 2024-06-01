# pysinergia\interfaces\web_flask.py

from pathlib import Path
from functools import wraps
import os

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
from pysinergia import (
    Constantes as _C,
    Funciones as _F,
    Json as _Json,
    ErrorPersonalizado as _ErrorPersonalizado,
    ErrorAutenticacion as _ErrorAutenticacion,
    ErrorDisco as _ErrorDisco,
    RegistradorLogs as _RegistradorLogs,
    Traductor as _Traductor,
)
from pysinergia.dominio import ModeloRespuesta
from pysinergia.web import (
    Comunicador as _Comunicador,
    Autenticador as _Autenticador,
)
from pysinergia import __version__ as api_motor

# --------------------------------------------------
# Clase: ServidorApi
# --------------------------------------------------
class ServidorApi:
    def __init__(mi, app_web:str, raiz_api:str=''):
        os.environ['RAIZ_API'] = raiz_api
        os.environ['APP_WEB'] = app_web
        mi.entorno:str = None

    # --------------------------------------------------
    # Métodos privados

    def _configurar_encabezados(mi, api:Flask):

        @api.after_request
        def procesar_salidas(respuesta:Response):
            respuesta.headers['X-API-Motor'] = f"{api_motor}"
            if mi.entorno == _C.ENTORNO.DESARROLLO and respuesta.status_code >= 200:
                content_type = str(respuesta.headers.get('Content-Type', ''))
                print(f'respuesta: {content_type} | {respuesta.content_type} | {respuesta.status_code}')
            return respuesta

        @api.before_request
        def procesar_entradas():
            if mi.entorno == _C.ENTORNO.DESARROLLO:
                content_type = str(request.headers.get('Content-Type', ''))
                if content_type:
                    print(f'peticion: {content_type}')

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

    def crear_api(mi, dir_frontend:str, alias_frontend:str, origenes_cors:list=['*'], titulo:str='', descripcion:str='', version:str='', doc:bool=False, entorno:str='') -> Flask:
        mi.dir_frontend = (Path(_F.obtener_ruta_raiz()) / f'{dir_frontend}').resolve()
        os.environ['ALIAS_FRONTEND'] = alias_frontend
        api = Flask(__name__,
            static_url_path=f"{str(os.getenv('RAIZ_API', ''))}/{alias_frontend}",
            static_folder=mi.dir_frontend.as_posix(),
        )
        mi.titulo = titulo
        mi.descripcion = descripcion
        mi.version = version
        mi.entorno = entorno
        api.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
        mi._configurar_cors(api, origenes_cors)
        mi._configurar_encabezados(api)
        mi._configurar_endpoints(api)
        api.app_context().push()
        return api

    def mapear_enrutadores(mi, api:Flask, ubicacion:str):
        import importlib
        ruta_ubicacion = Path(ubicacion)
        modulo_base = 'web_flask'
        try:
            directorios = [d for d in ruta_ubicacion.iterdir() if d.is_dir()]
        except Exception as e:
            print(e)
            return
        for directorio in directorios:
            try:
                nombre_servicio = directorio.name
                if (directorio / f'{modulo_base}.py').is_file():
                    enrutador = importlib.import_module(f'{ubicacion}.{nombre_servicio}.{modulo_base}')
                    api.register_blueprint(getattr(enrutador, 'enrutador'))
            except Exception as e:
                print(e)
                continue

    def iniciar_servicio(mi, app:Flask, host:str, puerto:int):
        if mi.entorno == _C.ENTORNO.DESARROLLO or mi.entorno == _C.ENTORNO.LOCAL:
            ssl_cert=Path('cert.pem')
            ssl_key=Path('key.pem')
            app.config['TEMPLATES_AUTO_RELOAD'] = True
            app.config['EXPLAIN_TEMPLATE_LOADING'] = True
            app.app_context().push()
            app.run(
                host=host,
                port=puerto,
                ssl_context=(ssl_cert, ssl_key),
                debug=True if mi.entorno == _C.ENTORNO.DESARROLLO else False
            )

    def manejar_errores(mi, api:Flask, dir_logs:str, registro_logs:str, idiomas_disponibles:list):
        from werkzeug.exceptions import (
            HTTPException,
            InternalServerError,
        )
        from pydantic import ValidationError

        @api.errorhandler(_ErrorPersonalizado)
        def _error_personalizado(exc:_ErrorPersonalizado):
            traductor = _Traductor({'dominio': exc.traduccion, 'idiomas_disponibles': idiomas_disponibles})
            salida = ModeloRespuesta(
                codigo=exc.codigo,
                tipo=exc.tipo,
                mensaje=exc.mensaje,
                detalles=exc.detalles,
                _=traductor.abrir_traduccion(request.headers.get('Accept-Language'))
            ).diccionario()
            if exc.tipo == _C.SALIDA.ERROR:
                nombre = registro_logs
                if exc.aplicacion and exc.servicio:
                    nombre = f'{exc.aplicacion}_{exc.servicio}'
                _RegistradorLogs.crear(f'{nombre}', 'ERROR', f'{dir_logs}/{nombre}.log').error(
                    f'{mi._obtener_url()} | {salida.__str__()}'
                )
            return Response(
                _Json.codificar(salida),
                status=exc.codigo,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(_ErrorAutenticacion)
        def _error_autenticacion(exc:_ErrorAutenticacion):
            if exc.url_login:
                return redirect(exc.url_login)
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            salida = ModeloRespuesta(
                codigo=exc.codigo,
                tipo=_C.SALIDA.ALERTA,
                mensaje=exc.mensaje,
                detalles=[],
                _=traductor.abrir_traduccion(request.headers.get('Accept-Language'))
            ).diccionario()
            return Response(
                _Json.codificar(salida),
                status=exc.codigo,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(_ErrorDisco)
        def _error_disco(exc:_ErrorDisco):
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            salida = ModeloRespuesta(
                codigo=exc.codigo,
                tipo='ERROR',
                mensaje=exc.mensaje,
                detalles=exc.detalles,
                _=traductor.abrir_traduccion(request.headers.get('Accept-Language'))
            ).diccionario()
            _RegistradorLogs.crear(f'{registro_logs}', 'ERROR', f'{dir_logs}/{registro_logs}.log').error(
                f'{mi._obtener_url()} | {salida.__str__()}'
            )
            return Response(
                _Json.codificar(salida),
                status=exc.codigo,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(ValidationError)
        def _error_validacion(exc:ValidationError):
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            errores = exc.errors()
            detalles = []
            for error in errores:
                detalles.append({
                    'tipo': error['type'],
                    'error': error['msg'],
                    'origen': error['loc'],
                    'valor': error['input']
                })
            salida = ModeloRespuesta(
                codigo=_C.ESTADO._422_NO_PROCESABLE,
                tipo=_C.SALIDA.ALERTA,
                mensaje='Los-datos-recibidos-son-invalidos',
                detalles=detalles,
                _=traductor.abrir_traduccion(request.headers.get('Accept-Language'))
            ).diccionario()
            if mi.entorno == _C.ENTORNO.DESARROLLO:
                _RegistradorLogs.crear(registro_logs, 'DEBUG', f'{dir_logs}/{registro_logs}.log').debug(exc, exc_info=True)
            return Response(
                _Json.codificar(salida),
                status=_C.ESTADO._422_NO_PROCESABLE,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(HTTPException)
        def _error_http(exc:HTTPException):
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            salida = ModeloRespuesta(
                codigo=exc.code,
                tipo=_F.tipo_salida(exc.code),
                mensaje=exc.description,
                _=traductor.abrir_traduccion(request.headers.get('Accept-Language'))
            ).diccionario()
            if exc.code >= 500:
                _RegistradorLogs.crear(registro_logs, 'ERROR', f'{dir_logs}/{registro_logs}.log').error(
                    f'{mi._obtener_url()} | {salida.__str__()}'
                )
            return Response(
                _Json.codificar(salida),
                status=exc.code,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(InternalServerError)
        def _error_interno(exc:InternalServerError):
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            descripcion = ''
            origen = exc.original_exception
            if origen.__doc__:
                descripcion = origen.__doc__
            if len(origen.args) > 0:
                descripcion = origen.args[0]
            salida = ModeloRespuesta(
                codigo=_C.ESTADO._500_ERROR,
                tipo=_F.tipo_salida(_C.ESTADO._500_ERROR),
                mensaje=descripcion,
                _=traductor.abrir_traduccion(request.headers.get('Accept-Language'))
            ).diccionario()
            _RegistradorLogs.crear(registro_logs, 'ERROR', f'{dir_logs}/{registro_logs}.log').error(
                f'{mi._obtener_url()} | {salida.__str__()}'
            )
            return Response(
                _Json.codificar(salida),
                status=_C.ESTADO._500_ERROR,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(Exception)
        def _error_nomanejado(exc:Exception):
            import sys
            traductor = _Traductor({'idiomas_disponibles': idiomas_disponibles})
            exception_type, exception_value, exception_traceback = sys.exc_info()
            exception_name = getattr(exception_type, '__name__', None)
            descripcion = f'<{exception_name}: {exception_value}>'
            salida = ModeloRespuesta(
                codigo=_C.ESTADO._500_ERROR,
                tipo=_C.SALIDA.ERROR,
                mensaje='Error-no-manejado',
                descripcion=descripcion,
                _=traductor.abrir_traduccion(request.headers.get('Accept-Language'))
            ).diccionario()
            registrador = _RegistradorLogs.crear(registro_logs, 'ERROR', f'{dir_logs}/{registro_logs}.log')
            if mi.entorno == _C.ENTORNO.DESARROLLO:
                registrador.error(exc, exc_info=True)
            else:
                registrador.error(f'{mi._obtener_url()} | {descripcion}')
            return Response(
                _Json.codificar(salida),
                status=_C.ESTADO._500_ERROR,
                mimetype=_C.MIME.JSON
            )


# --------------------------------------------------
# Clase: ComunicadorWeb
# --------------------------------------------------
class ComunicadorWeb(_Comunicador):

    # --------------------------------------------------
    # Métodos privados

    def _recibir_peticion(mi) -> dict:
        peticion = {}
        if request.form:
            for key in request.form:
                if request.files and key in request.files:
                    continue
                peticion[key] = request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form[key]
        if request.is_json:
            json = request.get_json(silent=True) or {}
            for key, value in json.items():
                peticion[key] = value
        if request.args:
            for key in request.args:
                peticion[key] = request.args.getlist(key) if len(request.args.getlist(key)) > 1 else request.args[key]
        return peticion

    # --------------------------------------------------
    # Métodos públicos

    def procesar_peticion(mi, idiomas_aceptados:str, sesion:dict=None):
        super().procesar_peticion(idiomas_aceptados, sesion)
        from urllib.parse import urlparse
        url_actual = str(request.base_url)
        url_analizada = urlparse(url_actual)
        raiz_api = mi.config_web.get('raiz_api')
        dir_frontend = mi.config_web.get('frontend')
        servidor = f'{url_analizada.scheme}://{url_analizada.netloc}'
        mi.contexto['url'] = {
            'servidor': servidor,
            'absoluta': url_actual,
            'relativa': url_analizada.path,
            'app': str(request.url_root).strip('/'),
            'puntofinal': request.path,
            'frontend': f'{raiz_api}/{dir_frontend}',
        }
        mi.contexto['web']['api_marco'] = 'Flask'
        mi.contexto['web']['dominio'] = url_analizada.hostname
        mi.contexto['web']['acepta'] = request.headers.get('accept', '')
        mi.contexto['peticion'] = mi._recibir_peticion()


# --------------------------------------------------
# Clase: AutenticadorWeb
# --------------------------------------------------
class AutenticadorWeb(_Autenticador):

    # --------------------------------------------------
    # Métodos privados

    def _validar_apikey(mi) -> str:
        if 'Authorization' in request.headers:
            api_key_header = request.headers.get('Authorization').replace('Bearer ', '')
            if mi.api_keys and api_key_header and api_key_header in mi.api_keys:
                return mi.api_keys.get(api_key_header)
        mensaje = 'API-key-invalida'
        raise _ErrorAutenticacion(
            mensaje=mensaje,
            codigo=_C.ESTADO._403_NO_AUTORIZADO,
        )
    
    def _validar_token(mi) -> str:
        mensaje = 'Encabezado-de-autorizacion-invalido'
        if 'X-Token' in request.headers:
            sesion_token_header = request.headers.get('X-Token')
            if sesion_token_header:
                mi.token = sesion_token_header
                if not mi._verificar_jwt():
                    mensaje = 'Token-invalido'
                else:
                    return mi.token
        raise _ErrorAutenticacion(
            mensaje=mensaje,
            codigo=_C.ESTADO._401_NO_AUTENTICADO,
            url_login=mi.url_login
        )

    # --------------------------------------------------
    # Métodos públicos

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

