# app.py

# --------------------------------------------------
# Script de inicio para Servidor Local
# --------------------------------------------------
framework = ''
entorno = 'DESARROLLO'

# --------------------------------------------------
# Importaciones de PySinergIA
if framework == 'fastapi':
    from pysinergia.web_fastapi import ServidorApi
else:
    from pysinergia.web_flask import ServidorApi

# --------------------------------------------------
# Configuración de la Api
titulo = 'Api Demo'
descripcion = """
Esta es una API REST básica implementada para demostrar las funciones de la biblioteca PySinergIA.
"""
version = '0.1.0'

origenes_cors = ['*']
registro_logs = 'api_demo'
alias_frontend = 'app'
dir_frontend = './frontend'
ubicacion_enrutadores = 'backend'

# --------------------------------------------------
# Creación de la Api
servidor = ServidorApi()
api = servidor.crear_api(dir_frontend, alias_frontend, origenes_cors, titulo, descripcion, version, doc=True)
servidor.mapear_enrutadores(api, ubicacion=ubicacion_enrutadores)
servidor.manejar_errores(api, registro_logs=registro_logs)

# --------------------------------------------------
# Lanzamiento del Servidor Web (local)
if __name__ == '__main__':
    servidor.iniciar_servicio(
        host='localhost', 
        puerto=8000 if framework=='fastapi' else 5000,
        app='app:api' if framework=='fastapi' else api,
        entorno=entorno
    )
