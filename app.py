# app.py

# --------------------------------------------------
# Script de inicio
# --------------------------------------------------

# --------------------------------------------------
# Configuración general de la Aplicacion
framework = 'flask'  # flask | fastapi
entorno = 'PRODUCCION'  # PRODUCCION o DESARROLLO
app_web = 'api' # App real en: CPanel/Python/Web Applications/Application URL = 'api'
raiz_api = ''  # Url relativa de la App (solo en desarrollo/local) = '/api'

# --------------------------------------------------
# Configuracion especifica de la Api
titulo = 'Api Demo'
descripcion = """
Esta es una API REST basica implementada para probar y demostrar las funciones de la biblioteca PySinergIA.
"""
version = '0.1.0'

ubicacion_enrutadores = 'backend'
alias_frontend = 'web'
dir_frontend = './frontend'
dir_logs = './logs'
registro_logs = 'api_demo'
idiomas = ['es','en']
origenes_cors = ['*']

# --------------------------------------------------
# Importaciones de PySinergIA
if framework == 'fastapi':
    from pysinergia.web_fastapi import ServidorApi
else:
    from pysinergia.web_flask import ServidorApi

# --------------------------------------------------
# Creacion de la Api
servidor = ServidorApi(app_web, raiz_api)
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
