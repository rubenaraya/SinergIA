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
        import pandas as pd
        import io, os
        from uuid import uuid4
        uuid = str(uuid4())
        ruta_aux = mi.obtener_ruta()
        ruta_csv = f'{ruta_aux}/{uuid}.csv'
        try:
            tabla = pd.read_html(io.StringIO(contenido), encoding='utf-8')[0]
            tabla.to_csv(
                ruta_csv,
                header=True,
                index=False,
                encoding='utf-8',
                quoting=1
            )
            with open(ruta_csv, 'rb') as f:
                csv_bytes = f.read()
                csv_io = io.BytesIO(csv_bytes)
            os.remove(ruta_csv)
            return csv_io
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error en ExportadorCsv',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO.HTTP_500_ERROR,
                detalles=[str(e)]
            )

