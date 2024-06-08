# app.py

from dotenv import dotenv_values
from pathlib import Path
import os

# --------------------------------------------------
# Carga configuracion en variables de entorno

archivo = Path('.config.env')
if archivo.exists() and archivo.is_file():
    claves = dotenv_values(archivo)
    for clave, valor in claves.items():
        os.environ[clave] = valor

# --------------------------------------------------
# Importa la biblioteca de PySinergIA

if os.getenv('FRAMEWORK') == 'fastapi':
    from pysinergia.interfaces.web_fastapi import ServidorApi
else:
    from pysinergia.interfaces.web_flask import ServidorApi

# --------------------------------------------------
# Ejecuta script de inicio

servidor = ServidorApi()
api = servidor.crear_api()
servidor.mapear_enrutadores(api)

# --------------------------------------------------
# Lanza el Servidor Web (solo en desarrollo/local)

if __name__ == '__main__':
    script = Path(__file__).stem
    servidor.iniciar_servicio(
        host = os.getenv('HOST_LOCAL'), 
        puerto = os.getenv('PUERTO_FASTAPI') if os.getenv('FRAMEWORK')=='fastapi' else os.getenv('PUERTO_FLASK'),
        app = f'{script}:api' if os.getenv('FRAMEWORK')=='fastapi' else api,
    )
