# app.py

# --------------------------------------------------
# Script de inicio
# --------------------------------------------------
framework = 'flask'
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

ubicacion_enrutadores = 'backend'
alias_frontend = 'app'
dir_frontend = './frontend'
dir_logs = './logs'
registro_logs = 'api_demo'
idiomas = ['es','en']
origenes_cors = ['*']

# --------------------------------------------------
# Creación de la Api
servidor = ServidorApi()
api = servidor.crear_api(dir_frontend, alias_frontend, origenes_cors, titulo, descripcion, version, doc=True)
servidor.mapear_enrutadores(api, ubicacion_enrutadores)
servidor.manejar_errores(api, dir_logs, registro_logs, idiomas)

# --------------------------------------------------
# Lanzamiento del Servidor Web
if __name__ == '__main__':
    servidor.iniciar_servicio(
        host='localhost', 
        puerto=8000 if framework=='fastapi' else 5000,
        app='app:api' if framework=='fastapi' else api,
        entorno=entorno
    )
