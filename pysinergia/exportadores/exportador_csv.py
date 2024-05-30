# pysinergia\exportadores\exportador_csv.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import Exportador as _Exportador
from pysinergia import (
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorCsv
# --------------------------------------------------
class ExportadorCsv(_Exportador):

    def generar(mi, contenido:str='', opciones:dict={}):
        from pathlib import Path
        from uuid import uuid4
        import pandas as pd
        import io
        uuid = str(uuid4())
        ruta_aux = Path(mi.obtener_ruta())
        ruta_csv = ruta_aux / f'{uuid}.csv'
        try:
            tabla = pd.read_html(io.StringIO(contenido), encoding='utf-8')[0]
            tabla.to_csv(
                ruta_csv,
                header=True,
                index=False,
                encoding='utf-8',
                quoting=1
            )
            csv_bytes = ruta_csv.read_bytes()
            csv_io = io.BytesIO(csv_bytes)
            ruta_csv.unlink()
            return csv_io
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error-en-exportador-CSV',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO._500_ERROR,
                detalles=[str(e)]
            )

