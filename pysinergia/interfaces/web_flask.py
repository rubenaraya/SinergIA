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
    ErrorPersonalizado as _ErrorPersonalizado
)
from pysinergia.dominio import Respuesta
from pysinergia.web import (
    Comunicador as _Comunicador,
    Autenticador as _Autenticador,
    ErrorAutenticacion as _ErrorAutenticacion,
    Traductor as _Traductor,
)
from pysinergia import __version__ as api_motor

# --------------------------------------------------
# Clase: ServidorApi
# --------------------------------------------------
class ServidorApi:
    def __init__(mi, ruta_script:str):
        ruta_script_path = Path(ruta_script)
        os.environ['RUTA_RAIZ'] = ruta_script_path.parent.as_posix()
        mi.nombre_script = ruta_script_path.stem

    # --------------------------------------------------
    # Métodos privados

    def _configurar_encabezados(mi, api:Flask):

        @api.after_request
        def procesar_salidas(respuesta:Response):
            respuesta.headers['X-API-Motor'] = f"{api_motor}"
            if os.getenv('ENTORNO') == _C.ENTORNO.DESARROLLO and respuesta.status_code >= 200:
                content_type = str(respuesta.headers.get('Content-Type', ''))
                print(f'respuesta: {content_type} | {respuesta.content_type} | {respuesta.status_code}')
            return respuesta

        @api.before_request
        def procesar_entradas():
            if os.getenv('ENTORNO') == _C.ENTORNO.DESARROLLO:
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

    def _configurar_cors(mi, api:Flask):
        from flask_cors import CORS
        CORS(api, resources={
                r'/*': {
                    'origins': os.getenv('ORIGENES_CORS'),
                    'methods': ['GET','POST','PUT','DELETE']
                }
            }
        )

    def _obtener_url(mi) -> str:
        url = f'{request.url}'
        return f'{request.method} {url}'

    def _manejar_errores(mi, api:Flask):
        from werkzeug.exceptions import (
            HTTPException,
            InternalServerError,
        )
        from pydantic import ValidationError

        @api.errorhandler(_ErrorAutenticacion)
        def _error_autenticacion(err:_ErrorAutenticacion):
            if err.url_login:
                return redirect(err.url_login)
            traductor = _Traductor({'idiomas_disponibles': os.getenv('IDIOMAS_DISPONIBLES')})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            respuesta = Respuesta(**err.serializar(), T=traductor)
            return Response(respuesta.json(), status=err.codigo, mimetype=_C.MIME.JSON)

        @api.errorhandler(_ErrorPersonalizado)
        def _error_personalizado(err:_ErrorPersonalizado):
            traductor = _Traductor({'dominio_idioma': err.dominio_idioma, 'idiomas_disponibles': os.getenv('IDIOMAS_DISPONIBLES')})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            respuesta = Respuesta(**err.serializar(), T=traductor)
            if err.conclusion == _C.CONCLUSION.ERROR:
                err.registrar(nombre=os.getenv('ARCHIVO_LOGS'), texto_extra=mi._obtener_url(), ruta_logs=os.getenv('RUTA_LOGS'))
            return Response(respuesta.json(), status=err.codigo, mimetype=_C.MIME.JSON)

        @api.errorhandler(ValidationError)
        def _error_validacion(err:ValidationError):
            traductor = _Traductor({'idiomas_disponibles': os.getenv('IDIOMAS_DISPONIBLES')})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            error = _ErrorPersonalizado(mensaje='Los-datos-recibidos-son-invalidos', codigo=_C.ESTADO._422_NO_PROCESABLE)
            error.agregar_detalles(err.errors())
            respuesta = Respuesta(**error.serializar(), T=traductor)
            if os.getenv('ENTORNO') == _C.ENTORNO.DESARROLLO:
                error.registrar(nombre=os.getenv('ARCHIVO_LOGS'), texto_extra=mi._obtener_url(), ruta_logs=os.getenv('RUTA_LOGS'), nivel_evento=_C.REGISTRO.DEBUG)
            return Response(respuesta.json(), status=_C.ESTADO._422_NO_PROCESABLE, mimetype=_C.MIME.JSON)

        @api.errorhandler(HTTPException)
        def _error_http(err:HTTPException):
            traductor = _Traductor({'idiomas_disponibles': os.getenv('IDIOMAS_DISPONIBLES')})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            error = _ErrorPersonalizado(mensaje=err.description, codigo=err.code)
            respuesta = Respuesta(**error.serializar(), T=traductor)
            if err.code >= 500:
                error.registrar(nombre=os.getenv('ARCHIVO_LOGS'), texto_extra=mi._obtener_url(), ruta_logs=os.getenv('RUTA_LOGS'))
            elif os.getenv('ENTORNO') == _C.ENTORNO.DESARROLLO:
                error.registrar(nombre=os.getenv('ARCHIVO_LOGS'), texto_extra=mi._obtener_url(), ruta_logs=os.getenv('RUTA_LOGS'), nivel_evento=_C.REGISTRO.DEBUG)

            return Response(respuesta.json(), status=err.code, mimetype=_C.MIME.JSON)

        @api.errorhandler(InternalServerError)
        def _error_interno(err:InternalServerError):
            traductor = _Traductor({'idiomas_disponibles': os.getenv('IDIOMAS_DISPONIBLES')})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))
            original = err.original_exception
            descripcion = original.args[0] if len(original.args) > 0 else original.__doc__ if original.__doc__ else ''
            error = _ErrorPersonalizado(mensaje=descripcion, codigo=_C.ESTADO._500_ERROR)
            respuesta = Respuesta(**error.serializar(), T=traductor)
            error.registrar(nombre=os.getenv('ARCHIVO_LOGS'), texto_extra=mi._obtener_url(), ruta_logs=os.getenv('RUTA_LOGS'))
            return Response(respuesta.json(), status=_C.ESTADO._500_ERROR, mimetype=_C.MIME.JSON)

        @api.errorhandler(Exception)
        def _error_nomanejado(err:Exception):
            traductor = _Traductor({'idiomas_disponibles': os.getenv('IDIOMAS_DISPONIBLES')})
            traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'))

            import sys
            exception_type, exception_value, exception_traceback = sys.exc_info()
            exception_name = getattr(exception_type, '__name__', None)
            print(f'{exception_name}: {exception_value}')

            mensaje = 'Error-no-manejado'
            error = _ErrorPersonalizado(mensaje=mensaje, codigo=_C.ESTADO._500_ERROR)
            respuesta = Respuesta(**error.serializar(), T=traductor)
            error.registrar(nombre=os.getenv('ARCHIVO_LOGS'), texto_extra=mi._obtener_url(), ruta_logs=os.getenv('RUTA_LOGS'))
            return Response(respuesta.json(), status=_C.ESTADO._500_ERROR, mimetype=_C.MIME.JSON)

    # --------------------------------------------------
    # Métodos públicos

    def crear_api(mi) -> Flask:
        dir_frontend = os.getenv('DIR_FRONTEND')
        mi.dir_frontend = (Path('.') / f'{dir_frontend}').resolve()
        api = Flask(__name__,
            static_url_path=f"{str(os.getenv('RAIZ_GLOBAL',''))}/{str(os.getenv('ALIAS_FRONTEND'))}",
            static_folder=mi.dir_frontend.as_posix(),
        )
        api.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
        mi._configurar_cors(api)
        mi._configurar_encabezados(api)
        mi._configurar_endpoints(api)
        mi._manejar_errores(api)
        api.app_context().push()
        return api

    def mapear_enrutadores(mi, api:Flask):
        import importlib
        ruta_backend = Path(os.getenv('DIR_BACKEND'))
        modulo_base = 'web_flask'
        try:
            directorios = [d for d in ruta_backend.iterdir() if d.is_dir()]
        except Exception as e:
            print(e)
            return
        for directorio in directorios:
            try:
                if (directorio / f'{modulo_base}.py').is_file():
                    dir_backend = os.getenv('DIR_BACKEND')
                    modulo = f'{dir_backend}.{directorio.name}.{modulo_base}'
                    enrutador = importlib.import_module(modulo)
                    api.register_blueprint(getattr(enrutador, 'enrutador'))
            except Exception as e:
                print(e)
                continue

    def iniciar_servicio(mi, app:Flask, puerto:int, host:str=None):
        if os.getenv('ENTORNO') == _C.ENTORNO.DESARROLLO or os.getenv('ENTORNO') == _C.ENTORNO.LOCAL:
            ssl_cert=str(Path(os.getenv('SSL_CERT')))
            ssl_key=str(Path(os.getenv('SSL_KEY')))
            if os.getenv('ENTORNO') == _C.ENTORNO.DESARROLLO:
                app.config['TEMPLATES_AUTO_RELOAD'] = True
                app.config['EXPLAIN_TEMPLATE_LOADING'] = True
            app.app_context().push()
            if not host:
                host = os.getenv('HOST_LOCAL')
            app.run(
                host=host,
                port=int(puerto),
                ssl_context=(ssl_cert, ssl_key),
                debug=os.getenv('MODO_DEBUG')
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
        url_analizada = urlparse(str(request.base_url))
        raiz_global = mi.config_web.get('RAIZ_GLOBAL','')
        alias_frontend = mi.config_web.get('ALIAS_FRONTEND')
        servidor = f'{url_analizada.scheme}://{url_analizada.netloc}'
        partes = url_analizada.path.lstrip('/').split('/')
        raiz_global = '/' + partes[0] if len(partes) > 0 else ''
        aplicacion = '/' + partes[1] if len(partes) > 1 else ''
        recurso = '/' + '/'.join(partes[2:]) if len(partes) > 2 else '/'
        mi.contexto['url'] = {
            'servidor': servidor,
            'absoluta': f'{servidor}{url_analizada.path}',
            'relativa': url_analizada.path,
            'puntoentrada': f'{servidor}{raiz_global}',
            'puntofinal': f'{aplicacion}{recurso}',
            'app': f'{raiz_global}{aplicacion}',
            'recurso': recurso,
            'frontend': f'{raiz_global}/{alias_frontend}',
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

