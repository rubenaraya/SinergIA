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
        nombre_archivo = opciones.get('nombre_archivo', '')
        if nombre_archivo and not str(nombre_archivo).endswith('.csv'):
            nombre_archivo = f'{nombre_archivo}.csv'
        ruta_destino = opciones.get('ruta_destino', '')
        ruta_archivo = f'{ruta_destino}/{nombre_archivo}'
        try:

            """
            salida_csv = ''
            with open(salida_csv, 'rb') as f:
                csv_bytes = f.read()
                csv_io = io.BytesIO(xlsx_bytes)
            return csv_io
            """
        except Exception as e:
            print(e)
            return None
