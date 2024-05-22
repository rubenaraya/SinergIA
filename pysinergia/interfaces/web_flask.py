# pysinergia\interfaces\web_flask.py

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
    RegistradorLogs as _RegistradorLogs,
)
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

    def _traspasar_traductor(mi, idiomas_aceptados:str, idiomas_disponibles:list, traduccion:str='base', dir_locales:str='./locales'):
        import gettext
        idioma = _F.negociar_idioma(idiomas_aceptados, idiomas_disponibles)
        t = gettext.translation(
            domain=traduccion,
            localedir=dir_locales,
            languages=[idioma],
            fallback=False,
        )
        return t.gettext

    # --------------------------------------------------
    # Métodos públicos

    def crear_api(mi, dir_frontend:str, alias_frontend:str, origenes_cors:list=['*'], titulo:str='', descripcion:str='', version:str='', doc:bool=False, entorno:str='') -> Flask:
        mi.dir_frontend = os.path.abspath(dir_frontend)
        os.environ['ALIAS_FRONTEND'] = alias_frontend
        api = Flask(__name__,
            static_url_path=f"{str(os.getenv('RAIZ_API', ''))}/{alias_frontend}",
            static_folder=mi.dir_frontend,
        )
        mi.titulo = titulo
        mi.descripcion = descripcion
        mi.version = version
        mi.entorno = entorno
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

    def iniciar_servicio(mi, app:Flask, host:str, puerto:int):
        if mi.entorno == _C.ENTORNO.DESARROLLO or mi.entorno == _C.ENTORNO.LOCAL:
            ssl_cert=os.path.join(os.path.abspath('.'), 'cert.pem')
            ssl_key=os.path.join(os.path.abspath('.'), 'key.pem')
            app.config['TEMPLATES_AUTO_RELOAD'] = True
            app.config['EXPLAIN_TEMPLATE_LOADING'] = True
            app.app_context().push()
            app.run(
                host=host,
                port=puerto,
                ssl_context=(ssl_cert, ssl_key),
                debug=True if mi.entorno == _C.ENTORNO.DESARROLLO else False
            )

    def manejar_errores(mi, api:Flask, dir_logs:str, registro_logs:str, idiomas:list):
        from werkzeug.exceptions import (
            HTTPException,
            InternalServerError,
        )
        from pydantic import ValidationError

        @api.errorhandler(_ErrorPersonalizado)
        def _error_personalizado(exc:_ErrorPersonalizado):
            _ = mi._traspasar_traductor(request.headers.get('Accept-Language'), idiomas)
            salida = _F.crear_salida(
                codigo=exc.codigo,
                tipo=exc.tipo,
                mensaje=_(exc.mensaje),
                detalles=exc.detalles
            )
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
            _ = mi._traspasar_traductor(request.headers.get('Accept-Language'), idiomas)
            salida = _F.crear_salida(
                codigo=exc.codigo,
                tipo=_C.SALIDA.ALERTA,
                mensaje=_(exc.mensaje),
                detalles=[]
            )
            return Response(
                _Json.codificar(salida),
                status=exc.codigo,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(ValidationError)
        def _error_validacion(exc:ValidationError):
            _ = mi._traspasar_traductor(request.headers.get('Accept-Language'), idiomas)
            errores = exc.errors()
            detalles = []
            for error in errores:
                detalles.append({
                    'tipo': _(error['type']),
                    'error': _(error['msg']),
                    'origen': error['loc'],
                    'valor': error['input']
                })
            salida = _F.crear_salida(
                codigo=_C.ESTADO.HTTP_422_NO_PROCESABLE,
                tipo=_C.SALIDA.ALERTA,
                mensaje=_('Los-datos-recibidos-son-invalidos'),
                detalles=detalles
            )
            if mi.entorno == _C.ENTORNO.DESARROLLO:
                _RegistradorLogs.crear(registro_logs, 'DEBUG', f'{dir_logs}/{registro_logs}.log').debug(exc, exc_info=True)
            return Response(
                _Json.codificar(salida),
                status=_C.ESTADO.HTTP_422_NO_PROCESABLE,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(HTTPException)
        def _error_http(exc:HTTPException):
            _ = mi._traspasar_traductor(request.headers.get('Accept-Language'), idiomas)
            salida = _F.crear_salida(
                codigo=exc.code,
                tipo=_F.tipo_salida(exc.code),
                mensaje=_(exc.description)
            )
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
            _ = mi._traspasar_traductor(request.headers.get('Accept-Language'), idiomas)
            descripcion = ''
            origen = exc.original_exception
            if origen.__doc__:
                descripcion = origen.__doc__
            if len(origen.args) > 0:
                descripcion = origen.args[0]
            salida = _F.crear_salida(
                codigo=_C.ESTADO.HTTP_500_ERROR,
                tipo=_F.tipo_salida(_C.ESTADO.HTTP_500_ERROR),
                mensaje=_(descripcion)
            )
            _RegistradorLogs.crear(registro_logs, 'ERROR', f'{dir_logs}/{registro_logs}.log').error(
                f'{mi._obtener_url()} | {salida.__str__()}'
            )
            return Response(
                _Json.codificar(salida),
                status=_C.ESTADO.HTTP_500_ERROR,
                mimetype=_C.MIME.JSON
            )

        @api.errorhandler(Exception)
        def _error_nomanejado(exc:Exception):
            import sys
            _ = mi._traspasar_traductor(request.headers.get('Accept-Language'), idiomas)
            texto = _('Error-no-manejado')
            exception_type, exception_value, exception_traceback = sys.exc_info()
            exception_name = getattr(exception_type, '__name__', None)
            mensaje = f'{texto} <{exception_name}: {exception_value}>'
            salida = _F.crear_salida(
                codigo=_C.ESTADO.HTTP_500_ERROR,
                tipo=_C.SALIDA.ERROR,
                mensaje=mensaje
            )
            registrador = _RegistradorLogs.crear(registro_logs, 'ERROR', f'{dir_logs}/{registro_logs}.log')
            if mi.entorno == _C.ENTORNO.DESARROLLO:
                registrador.error(exc, exc_info=True)
            else:
                registrador.error(f'{mi._obtener_url()} | {mensaje}')
            return Response(
                _Json.codificar(salida),
                status=_C.ESTADO.HTTP_500_ERROR,
                mimetype=_C.MIME.JSON
            )


# --------------------------------------------------
# Clase: ComunicadorWeb
# --------------------------------------------------
class ComunicadorWeb(_Comunicador):
    def __init__(mi, config:dict):
        mi.config:dict = config
        mi.idioma = None
        mi.traductor = None

    # --------------------------------------------------
    # Métodos públicos

    def agregar_contexto(mi, info:dict={}, sesion:dict={}) -> dict:
        global api_motor
        info['url'] = {
            'absoluta': request.base_url,
            'base': str(request.url_root).strip('/'),
            'relativa': request.path,
        }
        info['config'] = mi.config
        info['config']['ruta_raiz'] = _F.obtener_ruta_raiz()
        info['config']['idioma'] = mi.idioma
        info['config']['api_motor'] = api_motor
        info['sesion'] = sesion
        info['fecha'] = _F.fecha_hora(zona_horaria=mi.config.get('zona_horaria'))
        return info

    def generar_encabezados(mi, tipo_mime:str, nombre_archivo:str='') -> dict:
        return {
            'Content-Type': tipo_mime,
            'Content-disposition': f'inline; filename={nombre_archivo}'
        }


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
            codigo=_C.ESTADO.HTTP_403_NO_AUTORIZADO,
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
            codigo=_C.ESTADO.HTTP_401_NO_AUTENTICADO,
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
