# pysinergia\exportadores\exportador_excel.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador

# --------------------------------------------------
# Clase: ExportadorExcel
# --------------------------------------------------
class ExportadorExcel(_I_Exportador):
    def __init__(mi, opciones:dict={}):
        mi.opciones:dict = opciones

    def generar(mi, contenido:str, destino:str=''):
        import pandas, io, os

        return ''
