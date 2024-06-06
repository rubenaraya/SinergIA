# pysinergia\exportadores\exportador_excel.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.exportadores.exportador import (
    Exportador as _Exportador,
    ErrorExportador as _ErrorExportador,
)
from pysinergia import (
    Constantes as _Constantes,
)

# --------------------------------------------------
# Clase: ExportadorExcel
# --------------------------------------------------
class ExportadorExcel(_Exportador):

    def generar(mi, contenido:str, opciones:dict={}):
        from pathlib import Path
        from uuid import uuid4
        import pandas as pd
        import io
        uuid = str(uuid4())
        ruta_aux = Path(mi.obtener_ruta())
        ruta_xlsx = ruta_aux / f'{uuid}.xlsx'
        tabla_datos = opciones.get('tabla_datos', 'Hoja1')
        try:
            tabla = pd.read_html(io.StringIO(contenido), encoding='utf-8')[0]
            tabla.to_excel(
                ruta_xlsx,
                sheet_name=tabla_datos,
                header=True,
                index=False,
            )
            xlsx_bytes = ruta_xlsx.read_bytes()
            xlsx_io = io.BytesIO(xlsx_bytes)
            ruta_xlsx.unlink()
            return xlsx_io
        except Exception as e:
            raise _ErrorExportador(
                mensaje='Error-en-exportador-Excel',
                codigo=_Constantes.ESTADO._500_ERROR,
                detalles=[str(e)]
            )

