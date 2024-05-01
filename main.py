# main.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.web import ServidorApi

# --------------------------------------------------
# Script de inicio para Servidor en Producción

origenes = ['*']
servidor = ServidorApi()
api = servidor.crear_api(origenes)
servidor.mapear_enrutadores(api, ubicacion='backend')
servidor.asignar_frontend(api, directorio='./frontend', alias='app')
servidor.manejar_errores(api, nombre_registrador='api_web')
