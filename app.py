# app.py

import os
from pysinergia._dependencias import crear_servidor_api

# --------------------------------------------------
# Ejecuta script de inicio del ServidorApi
servidor = crear_servidor_api(__file__, '.config.env')
api = servidor.crear_api()
servidor.mapear_microservicios(api)

# --------------------------------------------------
# Lanza el Servidor Web (solo en DESARROLLO/LOCAL)
if __name__ == '__main__':
    servidor.iniciar_servicio_web(
        host = os.getenv('HOST_LOCAL'), 
        puerto = os.getenv('PUERTO_FASTAPI') if os.getenv('FRAMEWORK')=='fastapi' else os.getenv('PUERTO_FLASK'),
        app = f'{servidor.nombre_script}:api' if os.getenv('FRAMEWORK')=='fastapi' else api,
    )
