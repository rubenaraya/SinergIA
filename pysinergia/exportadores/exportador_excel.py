# pysinergia\exportadores\exportador_excel.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador

# --------------------------------------------------
# Clase: ExportadorExcel
# --------------------------------------------------
class ExportadorExcel(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str, opciones:dict={}):
        import pandas as pd
        import io, os
        hoja_estilos = opciones.get('hoja_estilos', '')
        ruta_destino = opciones.get('ruta_destino', '')

        salida_xlsx = ''
        with open(salida_xlsx, 'rb') as f:
            xlsx_bytes = f.read()
            xlsx_io = io.BytesIO(xlsx_bytes)
        return xlsx_io

