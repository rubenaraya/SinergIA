# pysinergia\web\flask.py

import os
from pathlib import Path
from functools import wraps

# --------------------------------------------------
# Importaciones de Infraestructura Web

from flask import (
    Flask,
    Response,
    request,
    redirect,
    send_from_directory,
    jsonify,
)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes as C,
    ErrorPersonalizado,
)
from pysinergia.dominio import Respuesta
from pysinergia.web import (
    Comunicador,
    Autenticador,
    ErrorAutenticacion,
    Traductor,
)
from pysinergia import __pysinergia__

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
            global __pysinergia__
            respuesta.headers['X-API-Motor'] = __pysinergia__
            if os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO and respuesta.status_code >= 200:
                content_type = str(respuesta.headers.get('Content-Type', ''))
                print(f'respuesta: {content_type} | {respuesta.content_type} | {respuesta.status_code}')
            if respuesta.content_type == 'application/json':
                respuesta.headers['Content-Type'] = 'application/json; charset=utf-8'
            return respuesta

        @api.before_request
        def procesar_entradas():
            if os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO:
                content_type = str(request.headers.get('Content-Type', ''))
                if content_type:
                    print(f'peticion: {content_type}')

    def _configurar_endpoints(mi, api:Flask):
        global __pysinergia__

        @api.route('/', methods=['GET'])
        def entrypoint():
            return {'api-entrypoint': __pysinergia__}

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
        api.config['CORS_HEADERS'] = 'Content-Type'

    def _obtener_url(mi) -> str:
        url = f'{request.url}'
        return f'{request.method} {url}'

    def _crear_respuesta_error(mi, err:ErrorPersonalizado, registrar:bool=False):
        traductor = Traductor({'idiomas_disponibles': os.getenv('IDIOMAS_DISPONIBLES')})
        traductor.asignar_idioma(idiomas_aceptados=request.headers.get('Accept-Language'), dominio_idioma=err.dominio_idioma)
        respuesta = Respuesta(**err.serializar(), T=traductor).diccionario()
        if registrar:
            err.registrar(texto_pre=mi._obtener_url())
        return jsonify(respuesta), err.codigo

    def _manejar_errores(mi, api:Flask):
        from werkzeug.exceptions import (
            HTTPException,
            InternalServerError,
        )
        from pydantic import ValidationError

        @api.errorhandler(ErrorAutenticacion)
        def _error_autenticacion(err:ErrorAutenticacion):
            if err.url_login:
                return redirect(err.url_login)
            return mi._crear_respuesta_error(err, False)

        @api.errorhandler(ErrorPersonalizado)
        def _error_personalizado(err:ErrorPersonalizado):
            registrar = (err.conclusion == C.CONCLUSION.ERROR) or (os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO)
            return mi._crear_respuesta_error(err, registrar)

        @api.errorhandler(ValidationError)
        def _error_validacion(err:ValidationError):
            error = ErrorPersonalizado(mensaje='Los-datos-recibidos-son-invalidos', codigo=C.ESTADO._422_NO_PROCESABLE, nivel_evento=C.REGISTRO.INFO)
            error.agregar_detalles(err.errors())
            registrar = (os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO)
            return mi._crear_respuesta_error(error, registrar)

        @api.errorhandler(HTTPException)
        def _error_http(err:HTTPException):
            error = ErrorPersonalizado(mensaje=err.description, codigo=err.code, nivel_evento=C.REGISTRO.ERROR if err.code >= 500 else C.REGISTRO.DEBUG)
            registrar = (err.code >= 500) or (os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO)
            return mi._crear_respuesta_error(error, registrar)

        @api.errorhandler(InternalServerError)
        def _error_interno(err:InternalServerError):
            original = err.original_exception
            descripcion = original.args[0] if len(original.args) > 0 else original.__doc__ if original.__doc__ else ''
            error = ErrorPersonalizado(mensaje=descripcion, codigo=C.ESTADO._500_ERROR, nivel_evento=C.REGISTRO.ERROR)
            return mi._crear_respuesta_error(error, True)

        @api.errorhandler(Exception)
        def _error_nomanejado(err:Exception):
            import sys
            exception_type, exception_value, exception_traceback = sys.exc_info()
            exception_name = getattr(exception_type, '__name__', None)
            mensaje = f'{exception_name}: {exception_value}'
            error = ErrorPersonalizado(mensaje=mensaje, codigo=C.ESTADO._500_ERROR, nivel_evento=C.REGISTRO.ERROR)
            return mi._crear_respuesta_error(error, True)

    # --------------------------------------------------
    # Métodos públicos

    def crear_api(mi) -> Flask:
        dir_frontend = os.getenv('DIR_FRONTEND')
        mi.dir_frontend = (Path('.') / f'{dir_frontend}').resolve()
        api = Flask(__name__,
            static_url_path=f"{str(os.getenv('RAIZ_GLOBAL',''))}/{str(os.getenv('ALIAS_FRONTEND',''))}",
            static_folder=mi.dir_frontend.as_posix(),
        )
        api.config['MAX_CONTENT_LENGTH'] = 50 * C.PESO.MB
        mi._configurar_cors(api)
        mi._configurar_encabezados(api)
        mi._configurar_endpoints(api)
        mi._manejar_errores(api)
        api.app_context().push()
        return api

    def mapear_microservicios(mi, api:Flask):
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

    def iniciar_servicio_web(mi, app:Flask, puerto:int, host:str=None):
        if os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO or os.getenv('ENTORNO') == C.ENTORNO.LOCAL:
            ssl_cert=str(Path(os.getenv('SSL_CERT')))
            ssl_key=str(Path(os.getenv('SSL_KEY')))
            if os.getenv('ENTORNO') == C.ENTORNO.DESARROLLO:
                app.config['TEMPLATES_AUTO_RELOAD'] = True
                app.config['EXPLAIN_TEMPLATE_LOADING'] = True
                app.config['PROPAGATE_EXCEPTIONS'] = True
            app.app_context().push()
            app.test_request_context().push()
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
class ComunicadorWeb(Comunicador):

    # --------------------------------------------------
    # Métodos privados

    def _recibir_peticion(mi) -> dict:
        peticion = {}
        try:
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
        except Exception as e:
            pass
        return peticion

    # --------------------------------------------------
    # Métodos públicos

    def procesar_peticion(mi, idiomas_aceptados:str, sesion:dict=None):
        super().procesar_peticion(idiomas_aceptados, sesion)
        from urllib.parse import urlparse
        alias_frontend = mi.config_web.get('ALIAS_FRONTEND')
        url_analizada = urlparse(str(request.base_url))
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
        mi.contexto['web']['API_MARCO'] = 'Flask'
        mi.contexto['web']['DOMINIO'] = url_analizada.hostname
        mi.contexto['web']['ACEPTA'] = request.headers.get('accept', '')
        mi.contexto['peticion'] = mi._recibir_peticion()
        mi.contexto['cookies'] = {}
        if request.cookies:
            for nombre, valor in request.cookies.items():
                mi.contexto['cookies'][nombre] = valor

    def asignar_cookie(mi, respuesta:Response, nombre:str, valor:str, duracion:int=None):
        alcance = mi.contexto['url'].get('app') if mi.contexto.get('url') else '/'
        duracion = mi.config_web.get('DURACION_TOKEN') if not duracion else duracion
        respuesta.set_cookie(
            key=nombre,
            value=valor,
            max_age=duracion,
            path=alcance,
            secure=True,
            httponly=False
        )
        return respuesta


# --------------------------------------------------
# Clase: AutenticadorWeb
# --------------------------------------------------
class AutenticadorWeb(Autenticador):

    # --------------------------------------------------
    # Métodos privados

    def _validar_apikey(mi) -> str:
        if 'Authorization' in request.headers:
            api_key_header = request.headers.get('Authorization').replace('Bearer ', '')
            if mi.api_keys and api_key_header and api_key_header in mi.api_keys:
                return mi.api_keys.get(api_key_header)
        mensaje = 'API-key-invalida'
        raise ErrorAutenticacion(
            mensaje=mensaje,
            codigo=C.ESTADO._403_NO_AUTORIZADO,
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
        raise ErrorAutenticacion(
            mensaje=mensaje,
            codigo=C.ESTADO._401_NO_AUTENTICADO,
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

