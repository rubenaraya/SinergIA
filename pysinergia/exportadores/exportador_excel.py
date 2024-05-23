# pysinergia\exportadores\exportador_excel.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador
from pysinergia import (
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorExcel
# --------------------------------------------------
class ExportadorExcel(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str, opciones:dict={}):
        import pandas as pd
        import io
        nombre_archivo = opciones.get('nombre_archivo', '')
        if nombre_archivo and not str(nombre_archivo).endswith('.xlsx'):
            nombre_archivo = f'{nombre_archivo}.xlsx'
        ruta_destino = opciones.get('ruta_destino', '')
        ruta_archivo = f'{ruta_destino}/{nombre_archivo}'
        hoja_datos = opciones.get('hoja_datos', 'Hoja1')
        try:
            tabla = pd.read_html(io.StringIO(contenido), encoding='utf-8')[0]
            tabla.to_excel(
                ruta_archivo,
                sheet_name=hoja_datos,
                header=True,
                index=False,
            )
            with open(ruta_archivo, 'rb') as f:
                xlsx_bytes = f.read()
                xlsx_io = io.BytesIO(xlsx_bytes)
            return xlsx_io
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error en ExportadorExcel',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO.HTTP_500_ERROR,
                detalles=[str(e)]
            )

