# main.py

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia import (
    ServidorApi,
    Constantes,
)

# --------------------------------------------------
# Script de inicio

# Creación de la Api
origenes = ['*']
servidor = ServidorApi()
api = servidor.crear_api(origenes)
servidor.mapear_enrutadores(api, ubicacion='backend')
servidor.asignar_frontend(api, directorio='./frontend', alias='app')

# Inicio del Servidor local
if __name__ == '__main__':
    servidor.iniciar_servicio(
        app="app:api", 
        host='localhost', 
        puerto=8000, 
        modo=Constantes.MODO.PRODUCCION
    )
