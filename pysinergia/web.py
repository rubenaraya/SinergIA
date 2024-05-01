# pysinergia\web.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import (
    RequestValidationError,
    HTTPException,
)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Emisor
from pysinergia.globales import (
    Constantes,
    ErrorPersonalizado,
    RegistradorLogs,
)

# --------------------------------------------------
# Clase: ServidorApi
# --------------------------------------------------
class ServidorApi():

    # --------------------------------------------------
    # Métodos privados

    def _configurar_endpoints(mi, api:FastAPI):
        @api.get('/')
        def entrypoint():
            return {'entrypoint-api': 'SinergIA'}
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
            return Constantes.SALIDA.ERROR
        if estado < 300:
            return Constantes.SALIDA.EXITO
        if estado < 400:
            return Constantes.SALIDA.AVISO
        if estado < 500:
            return Constantes.SALIDA.ALERTA
        return Constantes.SALIDA.ERROR

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
        api.mount(f'/{alias}', StaticFiles(directory=f'{directorio}'), name='static')

    def mapear_enrutadores(mi, api:FastAPI, ubicacion:str):
        import importlib, os
        aplicaciones = os.listdir(ubicacion)
        for aplicacion in aplicaciones:
            if aplicacion != 'pysinergia':
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

    def manejar_errores(mi, api:FastAPI, nombre_registrador:str):

        @api.exception_handler(ErrorPersonalizado)
        async def _error_personalizado_handler(request:Request, exc:ErrorPersonalizado) -> JSONResponse:
            salida = mi._crear_salida(
                codigo=exc.codigo,
                tipo=exc.tipo,
                mensaje=exc.mensaje,
                detalles=exc.detalles
            )
            if exc.tipo == Constantes.SALIDA.ERROR:
                nombre = nombre_registrador
                if exc.aplicacion and exc.servicio:
                    nombre = f'{exc.aplicacion}_{exc.servicio}'
                RegistradorLogs.crear(f'{nombre}', 'ERROR', f'./logs/{nombre}.log').error(
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
                tipo=Constantes.SALIDA.ALERTA,
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
                RegistradorLogs.crear(nombre_registrador, 'ERROR', f'./logs/{nombre_registrador}.log').error(
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
                tipo=Constantes.SALIDA.ERROR,
                mensaje=mensaje
            )
            RegistradorLogs.crear(nombre_registrador, 'ERROR', f'./logs/{nombre_registrador}.log').error(
                f'{mi._obtener_url(request)} | {mensaje}'
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(salida)
            )


# --------------------------------------------------
# Clase: EmisorWeb
# --------------------------------------------------
"""
Falta que procese plantillas con Jinja2
Falta que pueda servir HTML
Falta que pueda servir archivos para descarga
"""
class EmisorWeb(I_Emisor):
    def __init__(mi):
        ...

    # --------------------------------------------------
    # Métodos públicos

    def entregar_respuesta(mi, resultado:dict):
        respuesta = resultado
        return respuesta

