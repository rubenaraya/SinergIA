# app.py

# --------------------------------------------------
# Script de inicio (produccion)
# --------------------------------------------------

# --------------------------------------------------
# Configuracion general de la Aplicacion
framework = 'flask'  # flask | fastapi
entorno = 'PRODUCCION'
app_web = 'api' # App real en: CPanel/Python/Web Applications/Application URL = 'api'
raiz_api = '' # Vacio!

# --------------------------------------------------
# Configuracion especifica de la Api
titulo = 'Api Demo'
descripcion = """
Esta es una API REST basica implementada para probar y demostrar las funciones de la biblioteca PySinergIA.
"""
version = '0.1.0'

ubicacion_enrutadores = 'backend'
alias_frontend = 'web'
dir_frontend = 'frontend'
dir_logs = 'logs'
archivo_logs = 'api_demo'
idiomas_disponibles = ['es','en']
origenes_cors = ['*']

# --------------------------------------------------
# Importaciones de PySinergIA
if framework == 'fastapi':
    from pysinergia.interfaces.web_fastapi import ServidorApi
else:
    from pysinergia.interfaces.web_flask import ServidorApi

# --------------------------------------------------
# Creacion de la Api
servidor = ServidorApi(app_web, raiz_api)
api = servidor.crear_api(dir_frontend, alias_frontend, origenes_cors, titulo, descripcion, version, doc=False, entorno=entorno)
servidor.mapear_enrutadores(api, ubicacion_enrutadores)
servidor.manejar_errores(api, dir_logs, archivo_logs, idiomas_disponibles)

