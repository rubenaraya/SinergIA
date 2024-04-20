# backend\pysinergia\interfaz.py

from fastapi import FastAPI

class Aplicacion():

    def __init__(mi, modo:str):
        mi.modo = modo

    def crear(mi, directorio:str) -> FastAPI:
        app = FastAPI()
        mi._configurar_entorno(app)
        mi._configurar_cors(app)
        mi._configurar_endpoints(app)
        mi._configurar_ruteadores(app)
        mi._configurar_directorio(app, directorio)
        mi._configurar_excepciones(app)
        mi._configurar_registrador(app)
        return app
    
    def lanzar(mi, app:FastAPI, host:str, port:int):
        import uvicorn
        if mi.modo == 'LOCAL' or mi.modo == 'DESARROLLO':
            uvicorn.run(app, 
                host = host,
                port = port, 
                ssl_keyfile = "./key.pem", 
                ssl_certfile = "./cert.pem"
            )

    def _configurar_endpoints(mi, app:FastAPI):
        @app.get('/')
        def home():
            return {'inicio-app': 'funcionando'}

    def _configurar_cors(mi, app:FastAPI):
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins = ['*'],
            allow_credentials = True,
            allow_methods = ["*"],
            allow_headers = ["*"],
        )

    def _configurar_directorio(mi, app:FastAPI, directorio:str):
        from fastapi.staticfiles import StaticFiles
        app.mount(
            f"/{directorio}",
            StaticFiles(directory = "./frontend"),
            name = "static"
        )


    def _configurar_entorno(mi, app:FastAPI):
        ...

    def _configurar_excepciones(mi, app:FastAPI):
        ...

    def _configurar_ruteadores(mi, app:FastAPI):
        ...

    def _configurar_registrador(mi, app:FastAPI):
        ...
