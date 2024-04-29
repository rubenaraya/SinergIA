# backend\pysinergia\web.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia.globales import Constantes
from backend.pysinergia.adaptadores import I_Emisor

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

    def iniciar_servicio(mi, app:str, host:str, puerto:int, modo:str):
        if modo == Constantes.MODO.LOCAL or modo == Constantes.MODO.DESARROLLO:
            import uvicorn
            uvicorn.run(
                app,
                host=host,
                port=puerto,
                ssl_keyfile="./key.pem",
                ssl_certfile="./cert.pem",
                reload=True
            )


# --------------------------------------------------
# Clase: EmisorWeb
# --------------------------------------------------
class EmisorWeb(I_Emisor):
    def __init__(mi):
        ...

    # --------------------------------------------------
    # Métodos públicos

    def entregar_respuesta(mi, resultado:dict):
        respuesta = resultado
        return respuesta


# --------------------------------------------------
# Clase: RegistradorLogs
# --------------------------------------------------
class RegistradorLogs():

    # --------------------------------------------------
    # Constantes
    class NIVEL:
        DEBUG = 10
        INFO = 20
        WARNING = 30
        ERROR = 40
        CRITICAL = 50

    # --------------------------------------------------
    # Métodos públicos

    def crear(mi, nombre:str, nivel:int, archivo:str):
        logging.basicConfig(
            level=nivel,
            filename=archivo,
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(module)s.%(funcName)s - %(message)s'
        )
        return logging.getLogger(nombre)
