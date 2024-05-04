# main.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.web import ServidorApi

# --------------------------------------------------
# Script de inicio Demo para Servidor en Producción
# --------------------------------------------------

# --------------------------------------------------
# Configuración de la Api
titulo = ''
descripcion = """
"""
version = ''

origenes_cors = ['*']
registro_logs = 'api_demo'
alias_frontend = 'app'
directorio_frontend = './frontend'
ubicacion_enrutadores = 'backend'

# --------------------------------------------------
# Creación de la Api
servidor = ServidorApi()
api = servidor.crear_api(titulo, descripcion, version, origenes_cors)
servidor.mapear_enrutadores(api, ubicacion=ubicacion_enrutadores)
servidor.asignar_frontend(api, directorio=directorio_frontend, alias=alias_frontend)
servidor.manejar_errores(api, registro_logs=registro_logs)
