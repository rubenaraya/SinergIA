# pysinergia\exportadores\exportador_csv.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador

# --------------------------------------------------
# Clase: ExportadorCsv
# --------------------------------------------------
class ExportadorCsv(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str='', opciones:dict={}):
        import pandas as pd
        import io, os
        hoja_estilos = opciones.get('hoja_estilos', '')
        ruta_destino = opciones.get('ruta_destino', '')

        salida_csv = ''
        with open(salida_csv, 'rb') as f:
            csv_bytes = f.read()
            csv_io = io.BytesIO(csv_bytes)
        return csv_io

