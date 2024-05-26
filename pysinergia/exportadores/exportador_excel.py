# pysinergia\exportadores\exportador_excel.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import Exportador as _Exportador
from pysinergia import (
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorExcel
# --------------------------------------------------
class ExportadorExcel(_Exportador):

    def generar(mi, contenido:str, opciones:dict={}):
        import pandas as pd
        import io, os
        from uuid import uuid4
        uuid = str(uuid4())
        tabla_datos = opciones.get('tabla_datos', 'Hoja1')
        ruta_aux = mi.obtener_ruta()
        ruta_xlsx = f'{ruta_aux}/{uuid}.xlsx'
        try:
            tabla = pd.read_html(io.StringIO(contenido), encoding='utf-8')[0]
            tabla.to_excel(
                ruta_xlsx,
                sheet_name=tabla_datos,
                header=True,
                index=False,
            )
            with open(ruta_xlsx, 'rb') as f:
                xlsx_bytes = f.read()
                xlsx_io = io.BytesIO(xlsx_bytes)
            os.remove(ruta_xlsx)
            return xlsx_io
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error en Exportador Excel',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO.HTTP_500_ERROR,
                detalles=[str(e)]
            )

