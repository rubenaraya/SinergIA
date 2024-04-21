# backend\pysinergia\infraestructura.py

from fastapi import FastAPI
import os
from backend.pysinergia.interfaces import ( I_EmisorRespuesta, I_ReceptorPeticion )

# --------------------------------------------------
# Clase: ServidorApi
# --------------------------------------------------
class ServidorApi():

    # --------------------------------------------------
    # Métodos privados
    # --------------------------------------------------

    def _configurar_endpoints(mi, api:FastAPI):
        @api.get('/')
        def entrypoint():
            return {'entrypoint-api': 'SinergIA'}
        @api.get('/favicon.ico')
        def favicon():
            return ''

    def _configurar_cors(mi, api:FastAPI):
        from fastapi.middleware.cors import CORSMiddleware
        api.add_middleware(
            CORSMiddleware,
            allow_origins = ['*'],
            allow_credentials = True,
            allow_methods = ["*"],
            allow_headers = ["*"],
        )

    def _configurar_directorio(mi, api:FastAPI, directorio:str, alias:str):
        from fastapi.staticfiles import StaticFiles
        api.mount(f"/{alias}", StaticFiles(directory=f"{directorio}"), name="static")

    # --------------------------------------------------
    # Métodos públicos
    # --------------------------------------------------

    def crear_api(mi, directorio:str, alias:str) -> FastAPI:
        api = FastAPI()
        mi._configurar_directorio(api, directorio, alias)
        mi._configurar_endpoints(api)
        mi._configurar_cors(api)
        return api

    def mapear_enrutadores(mi, api:FastAPI, ubicacion:str):
        import importlib
        aplicaciones = os.listdir(ubicacion)
        for aplicacion in aplicaciones:
            if aplicacion != 'pysinergia':
                servicios = os.listdir(f"{ubicacion}/{aplicacion}")
                for servicio in servicios:
                    ruta_archivo = os.path.join(ubicacion, aplicacion, servicio, 'enrutador.py')
                    if os.path.isfile(ruta_archivo):
                        enrutador = importlib.import_module(f"{ubicacion}.{aplicacion}.{servicio}.enrutador")
                        api.include_router(getattr(enrutador, 'enrutador'))

    def iniciar_servicio(mi, api:FastAPI, host:str, puerto:int, modo:str):
        import uvicorn
        if modo == 'LOCAL' or modo == 'DESARROLLO':
            uvicorn.run(api, host=host, port=puerto, ssl_keyfile="./key.pem", ssl_certfile="./cert.pem")


# --------------------------------------------------
# Clase: Enrutador
# --------------------------------------------------
class Enrutador():
    def __init__(mi):
        ...
    # --------------------------------------------------
    # Métodos privados
    # --------------------------------------------------
    # --------------------------------------------------
    # Métodos públicos
    # --------------------------------------------------


# --------------------------------------------------
# Clase: ReceptorPeticion
# --------------------------------------------------
class ReceptorPeticion(I_ReceptorPeticion):
    def __init__(mi):
        ...
    # --------------------------------------------------
    # Métodos privados
    # --------------------------------------------------
    # --------------------------------------------------
    # Métodos públicos
    # --------------------------------------------------
    def recibir_peticion(mi) -> dict:
        ...


# --------------------------------------------------
# Clase: EmisorRespuesta
# --------------------------------------------------
class EmisorRespuesta(I_EmisorRespuesta):
    def __init__(mi):
        ...
    # --------------------------------------------------
    # Métodos privados
    # --------------------------------------------------
    # --------------------------------------------------
    # Métodos públicos
    # --------------------------------------------------
    def crear_respuesta(mi) -> str:
        ...
