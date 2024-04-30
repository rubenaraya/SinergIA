# backend\pysinergia\web.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia.adaptadores import I_Emisor

class ExternalError(Exception):
    pass

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
            allow_methods = ["*"],
            allow_headers = ["*"],
        )

    # --------------------------------------------------
    # Métodos públicos

    def crear_api(mi, origenes:list) -> FastAPI:
        api = FastAPI()
        mi._configurar_endpoints(api)
        mi._configurar_cors(api, origenes)
        return api

    def asignar_frontend(mi, api:FastAPI, directorio:str, alias:str):
        api.mount(f"/{alias}", StaticFiles(directory=f"{directorio}"), name="static")

    def mapear_enrutadores(mi, api:FastAPI, ubicacion:str):
        import importlib, os
        aplicaciones = os.listdir(ubicacion)
        for aplicacion in aplicaciones:
            if aplicacion != 'pysinergia':
                servicios = os.listdir(f"{ubicacion}/{aplicacion}")
                for servicio in servicios:
                    try:
                        ruta_archivo = os.path.join(ubicacion, aplicacion, servicio, 'web.py')
                        if os.path.isfile(ruta_archivo):
                            enrutador = importlib.import_module(f"{ubicacion}.{aplicacion}.{servicio}.web")
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
            ssl_keyfile="./key.pem",
            ssl_certfile="./cert.pem",
            reload=True
        )

    def manejar_errores(mi, api:FastAPI):

        @api.exception_handler(ExternalError)
        async def external_exception_handler(request:Request, exc:ExternalError) -> JSONResponse:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Algo salió mal"},
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
