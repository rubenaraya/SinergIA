# pysinergia\exportadores\exportador_excel.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador
from pysinergia import Funciones as _Funciones

# --------------------------------------------------
# Clase: ExportadorExcel
# --------------------------------------------------
class ExportadorExcel(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str, opciones:dict={}):
        import pandas as pd
        import io, os
        nombre_archivo = opciones.get('nombre_archivo', '')
        if nombre_archivo and not str(nombre_archivo).endswith('.xlsx'):
            nombre_archivo = f'{nombre_archivo}.xlsx'
        ruta_destino = opciones.get('ruta_destino', '')
        ruta_archivo = f'{ruta_destino}/{nombre_archivo}'
        hoja_estilos = opciones.get('hoja_estilos', '')

        """
        salida_xlsx = ''
        with open(salida_xlsx, 'rb') as f:
            xlsx_bytes = f.read()
            xlsx_io = io.BytesIO(xlsx_bytes)
        return xlsx_io
        """
