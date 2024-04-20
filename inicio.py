# main.py

from backend.pysinergia.interfaz import ServidorApi

# Creación de la Api
servidor = ServidorApi(modo='DESARROLLO', registro='DEBUG')
api = servidor.crear_api(directorio='./frontend', alias='frontend', prefijo='apps')
servidor.mapear_servicios(api, ubicacion='backend')

# Inicio del Servidor local
if __name__ == '__main__':
    servidor.lanzar(api, host='localhost', puerto=8000)

