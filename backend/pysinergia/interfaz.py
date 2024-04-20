# backend\pysinergia\interfaz.py

from fastapi import FastAPI
import os

class ServidorApi():

    def __init__(mi, modo:str='PRODUCCION', registro:str='ERROR'):
        mi.modo = modo
        mi.registro = registro
        mi.prefijo = ''

    def _configurar_endpoints(mi, api:FastAPI):
        @api.get('/')
        def home():
            return {'entrypoint-api': 'SinergIA'}

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
        api.mount(
            f"/{alias}",
            StaticFiles(directory = f"{directorio}"),
            name = "static"
        )

    def _configurar_entorno(mi, api:FastAPI):
        from dotenv import dotenv_values
        archivos = {
            'DESARROLLO': ".desarrollo.env",
            'PRUEBAS': ".pruebas.env",
            'PRODUCCION': ".produccion.env",
            'LOCAL': ".local.env"
        }
        ruta_archivo = os.path.join(os.path.abspath("."), archivos.get(mi.modo))
        if os.path.isfile(ruta_archivo):
            claves = dotenv_values(ruta_archivo)
            for clave, valor in claves.items():
                # print(f"{clave}={valor}")
                ...

    def crear_api(mi, directorio:str, alias:str, prefijo:str='') -> FastAPI:
        mi.prefijo = prefijo
        api = FastAPI()
        mi._configurar_directorio(api, directorio, alias)
        mi._configurar_endpoints(api)
        mi._configurar_cors(api)
        return api

    def mapear_servicios(mi, api:FastAPI, ubicacion:str):
        import importlib
        directorios = os.listdir(ubicacion)
        for directorio in directorios:
            if directorio != 'pysinergia':
                subdirectorios = os.listdir(f"{ubicacion}/{directorio}")
                for subdirectorio in subdirectorios:
                    ruta_archivo = os.path.join(ubicacion, directorio, subdirectorio, 'enrutador.py')
                    if os.path.isfile(ruta_archivo):
                        componente = importlib.import_module(f"{ubicacion}.{directorio}.{subdirectorio}.enrutador")
                        api.include_router(getattr(componente, 'enrutador'))

    def lanzar(mi, api:FastAPI, host:str, puerto:int):
        import uvicorn
        if mi.modo == 'LOCAL' or mi.modo == 'DESARROLLO':
            uvicorn.run(api, 
                host = host,
                port = puerto, 
                ssl_keyfile = "./key.pem", 
                ssl_certfile = "./cert.pem"
            )
