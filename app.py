# --------------------------------------------------
# app.py
# --------------------------------------------------

from pysinergia.web.base import configurar_servidor_api

# Script de inicio (Aplicación Global)
servidor = configurar_servidor_api(__file__)
api = servidor.crear_api()
servidor.mapear_microservicios(api)

# Lanza el Servidor Web (solo en DESARROLLO o LOCAL)
if __name__ == '__main__':
    import os
    servidor.iniciar_servicio_web(
        host = os.getenv('HOST_LOCAL'), 
        puerto = os.getenv('PUERTO_FASTAPI') if os.getenv('FRAMEWORK')=='fastapi' else os.getenv('PUERTO_FLASK'),
        app = f'{servidor.nombre_script}:api' if os.getenv('FRAMEWORK')=='fastapi' else api,
    )
