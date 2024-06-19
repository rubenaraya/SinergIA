# pysinergia\complementos\exportador_csv.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.complementos.exportador import (
    Exportador,
    ErrorExportador,
)
from pysinergia import Constantes

# --------------------------------------------------
# Clase: ExportadorCsv
# --------------------------------------------------
class ExportadorCsv(Exportador):

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
            csv_buffer = io.StringIO()
            tabla.to_csv(
                csv_buffer,
                header=True,
                index=False,
                encoding='utf-8-sig',
                quoting=0,
                sep=';'
            )
            csv_buffer.seek(0)
            with ruta_csv.open('w', encoding='utf-8-sig', newline='') as f:
                f.write(csv_buffer.read())
            csv_bytes = ruta_csv.read_bytes()
            csv_io = io.BytesIO(csv_bytes)
            ruta_csv.unlink()
            return csv_io
        except Exception as e:
            raise ErrorExportador(
                mensaje='Error-en-exportador-CSV',
                codigo=Constantes.ESTADO._500_ERROR,
                detalles=[str(e)],
                tipo=type(e),
            )

