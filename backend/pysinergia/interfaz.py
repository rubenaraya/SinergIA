# backend\pysinergia\interfaz.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

class Aplicacion():
    def crear(dir_static:str) -> FastAPI:
        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins = ['*'],
            allow_credentials = True,
            allow_methods = ["*"],
            allow_headers = ["*"],
        )
        app.mount(
            f"/{dir_static}",
            StaticFiles(directory = "./frontend"),
            name = "static"
        )

        # variables env a app.config
        # logger
        # excepciones

        # Endpoints de la Aplicación
        @app.get('/')
        def home():
            return {'inicio': 'funcionando'}

        return app
