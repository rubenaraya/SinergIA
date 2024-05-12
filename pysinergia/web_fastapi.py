# pysinergia\web_fastapi.py

from typing import Dict
import time, jwt, os

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import (
    FastAPI,
    Request,
    Response,
    Security,
)
from fastapi.responses import (
    JSONResponse,
    RedirectResponse,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import (
    APIKeyHeader,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import (
    RequestValidationError,
    HTTPException,
)
from jinja2 import (
    Environment,
    FileSystemLoader,
)
from functools import lru_cache

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
from pysinergia.adaptadores import Configuracion as _Configuracion
from pysinergia import __version__ as api_motor

# --------------------------------------------------
# Clase: ServidorApi
# --------------------------------------------------
class ServidorApi:

    # --------------------------------------------------
    # Métodos privados

    def _configurar_encabezados(mi, api:FastAPI):
        @api.middleware("http")
        async def configurar_encabezados_(request:Request, call_next):
            inicio = time.time()
            respuesta:Response = await call_next(request)
            tiempo_proceso = str(round(time.time() - inicio, 3))
            respuesta.headers["X-Tiempo-Proceso"] = tiempo_proceso
            respuesta.headers["X-API-Motor"] = api_motor
            return respuesta

    def _configurar_endpoints(mi, api:FastAPI):

        @api.get('/')
        def entrypoint():
            return {'api-entrypoint': f'{api_motor}'}

        @api.get('/favicon.ico')
        def favicon():
            return ''

    def _configurar_cors(mi, api:FastAPI, origenes_cors:list):
        api.add_middleware(
            CORSMiddleware,
            allow_origins = origenes_cors,
            allow_credentials = True,
            allow_methods = ['*'],
            allow_headers = ['*'],
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
            return _C.SALIDA.ERROR
        if estado < 300:
            return _C.SALIDA.EXITO
        if estado < 400:
            return _C.SALIDA.AVISO
        if estado < 500:
            return _C.SALIDA.ALERTA
        return _C.SALIDA.ERROR

    def _obtener_url(mi, request:Request) -> str:
        url = f'{request.url.path}?{request.query_params}' if request.query_params else request.url.path
        return f'{request.method} {url}'

    # --------------------------------------------------
    # Métodos públicos

    def crear_api(mi, dir_frontend:str, alias_frontend:str, origenes_cors:list=['*'], titulo:str='', descripcion:str='', version:str='', doc:bool=False) -> FastAPI:
        docs_url = '/docs' if doc else None
        redoc_url = '/redoc' if doc else None
        api = FastAPI(
            title=titulo,
            description=descripcion,
            version=version,
            docs_url=docs_url,
            redoc_url=redoc_url,
        )
        api.mount(f'/{alias_frontend}', StaticFiles(directory=f'{dir_frontend}'), name='frontend')
        mi._configurar_cors(api, origenes_cors)
        mi._configurar_encabezados(api)
        mi._configurar_endpoints(api)
        return api

    def mapear_enrutadores(mi, api:FastAPI, ubicacion:str):
        import importlib
        servicios = os.listdir(ubicacion)
        modulo_base = 'web_fastapi'
        for servicio in servicios:
            try:
                ruta_modulo = os.path.join(ubicacion, servicio, f'{modulo_base}.py')
                if os.path.isfile(ruta_modulo):
                    enrutador = importlib.import_module(f'{ubicacion}.{servicio}.{modulo_base}')
                    api.include_router(getattr(enrutador, 'enrutador'))
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

    def manejar_errores(mi, api:FastAPI, registro_logs:str):

        @api.exception_handler(_ErrorPersonalizado)
        async def _error_personalizado_handler(request:Request, exc:_ErrorPersonalizado) -> JSONResponse:
            salida = mi._crear_salida(
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
                    f'{mi._obtener_url(request)} | {salida.__repr__()}'
                )
            return JSONResponse(
                status_code=exc.codigo,
                content=jsonable_encoder(salida)
            )

        @api.exception_handler(_ErrorAutenticacion)
        async def _error_autenticacion_handler(request:Request, exc:_ErrorAutenticacion):
            salida = mi._crear_salida(
                codigo=exc.codigo,
                tipo=_C.SALIDA.ALERTA,
                mensaje=exc.mensaje,
                detalles=[]
            )
            if exc.url_login:
                return RedirectResponse(url=exc.url_login)
            return JSONResponse(
                status_code=exc.codigo,
                content=jsonable_encoder(salida)
            )

        @api.exception_handler(RequestValidationError)
        async def _request_validation_exception_handler(request:Request, exc:RequestValidationError) -> JSONResponse:
            errores = exc.errors()
            detalles = []
            for error in errores:
                detalles.append({
                    'error': error['msg'],
                    'origen': error['loc'],
                    'valor': error['input']
                })
            salida = mi._crear_salida(
                codigo=_C.ESTADO.HTTP_422_NO_PROCESABLE,
                tipo=_C.SALIDA.ALERTA,
                mensaje='Los datos recibidos no fueron procesados correctamente',
                detalles=detalles
            )
            return JSONResponse(
                status_code=_C.ESTADO.HTTP_422_NO_PROCESABLE,
                content=jsonable_encoder(salida)
            )

        @api.exception_handler(HTTPException)
        async def _http_exception_handler(request:Request, exc:HTTPException) -> JSONResponse:
            salida = mi._crear_salida(
                codigo=exc.status_code,
                tipo=mi._tipo_salida(exc.status_code),
                mensaje=exc.detail
            )
            if exc.status_code >= 500:
                _RegistradorLogs.crear(registro_logs, 'ERROR', f'./logs/{registro_logs}.log').error(
                    f'{mi._obtener_url(request)} | {salida.__repr__()}'
                )
            return JSONResponse(
                status_code=exc.status_code,
                content=jsonable_encoder(salida)
            )

        @api.exception_handler(Exception)
        async def _unhandled_exception_handler(request:Request, exc:Exception) -> JSONResponse:
            import sys
            exception_type, exception_value, exception_traceback = sys.exc_info()
            exception_name = getattr(exception_type, '__name__', None)
            mensaje = f'Error interno del Servidor <{exception_name}: {exception_value}>'
            salida = mi._crear_salida(
                codigo=_C.ESTADO.HTTP_500_ERROR,
                tipo=_C.SALIDA.ERROR,
                mensaje=mensaje
            )
            _RegistradorLogs.crear(registro_logs, 'ERROR', f'./logs/{registro_logs}.log').error(
                f'{mi._obtener_url(request)} | {mensaje}'
            )
            return JSONResponse(
                status_code=_C.ESTADO.HTTP_500_ERROR,
                content=jsonable_encoder(salida)
            )


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
            resultado = resultado.replace('{ruta_raiz}', _F.obtener_ruta_raiz())
        return resultado


# --------------------------------------------------
# Clase: AutenticadorWeb
# --------------------------------------------------
class AutenticadorWeb(HTTPBearer):
    def __init__(mi, secreto:str, algoritmo:str='HS256', url_login:str=None, api_keys:dict={}):
        super(AutenticadorWeb, mi).__init__(auto_error=False)
        mi.secreto = secreto
        mi.algoritmo = algoritmo
        mi.url_login:str = url_login
        mi.api_keys:dict = api_keys
        mi.token:str = None

    async def __call__(mi, request:Request):
        credentials:HTTPAuthorizationCredentials = await super(AutenticadorWeb, mi).__call__(request)
        mensaje = ''
        if credentials:
            if not credentials.scheme == 'Bearer':
                mensaje = 'Esquema de autenticación no válido.'
            else:
                mi.token = credentials.credentials
                if not mi._verificar_jwt():
                    mensaje = 'Token no válido o caducado.'
                else:
                    return mi.token
        else:
            mensaje = 'Código de autorización no válido.'
        raise _ErrorAutenticacion(mensaje=mensaje, codigo=_C.ESTADO.HTTP_401_NO_AUTENTICADO, url_login=mi.url_login)

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

    def validar_apikey(mi, api_key_header:str=Security(APIKeyHeader(name='X-API-Key'))) -> str:
        if mi.api_keys:
            if api_key_header in mi.api_keys:
                return mi.api_keys.get(api_key_header)
            raise _ErrorAutenticacion(
                codigo=_C.ESTADO.HTTP_401_NO_AUTENTICADO,
                mensaje='API key no válida'
            )
        return None


@lru_cache
def obtener_config(modelo:_Configuracion, modulo:str, aplicacion:str, entorno:str=None):
    archivo_env = _F.obtener_ruta_env(modulo, entorno)
    config:_Configuracion = modelo(_env_file=archivo_env)
    config.reconocer_servicio(archivo_env, aplicacion)
    return config
