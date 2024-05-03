# pysinergia\web.py

from typing import Dict
import time, jwt

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import (
    FastAPI,
    Request,
    status,
    Security,
)
from fastapi.responses import (
    JSONResponse,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
    RegistradorLogs as _RegistradorLogs,
)
from pysinergia import __version__

# --------------------------------------------------
# Clase: ServidorApi
# --------------------------------------------------
class ServidorApi:

    # --------------------------------------------------
    # Métodos privados

    def _configurar_endpoints(mi, api:FastAPI):
        @api.middleware("http")
        async def version_header(request:Request, call_next):
            response = await call_next(request)
            response.headers["x-api-version"] = __version__
            return response

        @api.get('/')
        def entrypoint():
            return {'api-entrypoint': f'{__version__}'}
        @api.get('/favicon.ico')
        def favicon():
            return ''

    def _configurar_cors(mi, api:FastAPI, origenes:list):
        api.add_middleware(
            CORSMiddleware,
            allow_origins = origenes,
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
            return _Constantes.SALIDA.ERROR
        if estado < 300:
            return _Constantes.SALIDA.EXITO
        if estado < 400:
            return _Constantes.SALIDA.AVISO
        if estado < 500:
            return _Constantes.SALIDA.ALERTA
        return _Constantes.SALIDA.ERROR

    def _obtener_url(mi, request:Request) -> str:
        url = f'{request.url.path}?{request.query_params}' if request.query_params else request.url.path
        return f'{request.method} {url}'

    # --------------------------------------------------
    # Métodos públicos

    def crear_api(mi, origenes:list) -> FastAPI:
        api = FastAPI()
        mi._configurar_endpoints(api)
        mi._configurar_cors(api, origenes)
        return api

    def asignar_frontend(mi, api:FastAPI, directorio:str, alias:str):
        api.mount(f'/{alias}', StaticFiles(directory=f'{directorio}'), name='frontend')

    def mapear_enrutadores(mi, api:FastAPI, ubicacion:str):
        import importlib, os
        aplicaciones = os.listdir(ubicacion)
        for aplicacion in aplicaciones:
            servicios = os.listdir(f'{ubicacion}/{aplicacion}')
            for servicio in servicios:
                try:
                    ruta_archivo = os.path.join(ubicacion, aplicacion, servicio, 'web.py')
                    if os.path.isfile(ruta_archivo):
                        enrutador = importlib.import_module(f'{ubicacion}.{aplicacion}.{servicio}.web')
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

    def manejar_errores(mi, api:FastAPI, registro:str):

        @api.exception_handler(_ErrorPersonalizado)
        async def _error_personalizado_handler(request:Request, exc:_ErrorPersonalizado) -> JSONResponse:
            salida = mi._crear_salida(
                codigo=exc.codigo,
                tipo=exc.tipo,
                mensaje=exc.mensaje,
                detalles=exc.detalles
            )
            if exc.tipo == _Constantes.SALIDA.ERROR:
                nombre = registro
                if exc.aplicacion and exc.servicio:
                    nombre = f'{exc.aplicacion}_{exc.servicio}'
                _RegistradorLogs.crear(f'{nombre}', 'ERROR', f'./logs/{nombre}.log').error(
                    f'{mi._obtener_url(request)} | {salida.__repr__()}'
                )
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
                codigo=status.HTTP_422_UNPROCESSABLE_ENTITY,
                tipo=_Constantes.SALIDA.ALERTA,
                mensaje='Los datos recibidos no fueron procesados correctamente',
                detalles=detalles
            )
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
                _RegistradorLogs.crear(registro, 'ERROR', f'./logs/{registro}.log').error(
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
                codigo=status.HTTP_500_INTERNAL_SERVER_ERROR,
                tipo=_Constantes.SALIDA.ERROR,
                mensaje=mensaje
            )
            _RegistradorLogs.crear(registro, 'ERROR', f'./logs/{registro}.log').error(
                f'{mi._obtener_url(request)} | {mensaje}'
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(salida)
            )


# --------------------------------------------------
# Clase: ComunicadorWeb
# --------------------------------------------------
class ComunicadorWeb():
    def __init__(mi, api_keys:dict={}):
        mi.api_keys = api_keys

    # --------------------------------------------------
    # Métodos públicos

    def validar_apikey(mi, api_key_header:str=Security(APIKeyHeader(name='X-API-Key'))) -> str:
        if mi.api_keys:
            if api_key_header in mi.api_keys:
                return mi.api_keys.get(api_key_header)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='API key no válida'
            )
        return None

    def transformar_contenido(mi, request:Request, contenido:dict={}, plantilla:str='', directorio:str=''):
        plantillas = Jinja2Templates(directory=directorio)
        contenido['request'] = request
        resultado = plantillas.TemplateResponse(
            name=plantilla,
            context=contenido
        )
        return resultado


# --------------------------------------------------
# Clase: AutenticadorJWT
# --------------------------------------------------
class AutenticadorJWT(HTTPBearer):
    def __init__(mi, secreto:str, algoritmo:str='HS256', auto_error:bool=True):
        super(AutenticadorJWT, mi).__init__(auto_error=auto_error)
        mi.secreto = secreto
        mi.algoritmo = algoritmo
        mi.token:str = None

    async def __call__(mi, request:Request):
        credentials:HTTPAuthorizationCredentials = await super(AutenticadorJWT, mi).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Esquema de autenticación no válido.')
            mi.token = credentials.credentials
            if not mi._verificar_jwt():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token no válido o caducado.')
            return mi.token
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Código de autorización no válido.')

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

    def obtener_id_usuario(mi):
        token_decodificado = mi._decodificar_jwt()
        if token_decodificado:
            return token_decodificado.get('id_usuario')
        return ''

    def firmar_jwt(mi, id_usuario:str, duracion:int=30) -> str:
        payload = {
            'id_usuario': id_usuario,
            'caducidad': time.time() + 60 * duracion
        }
        token = jwt.encode(payload, mi.secreto, algorithm=mi.algoritmo)
        return token

