# pysinergia\exportadores\exportador_csv.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador
from pysinergia import (
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorCsv
# --------------------------------------------------
class ExportadorCsv(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str='', opciones:dict={}):
        import pandas as pd
        import io
        nombre_archivo = opciones.get('nombre_archivo', '')
        if nombre_archivo and not str(nombre_archivo).endswith('.csv'):
            nombre_archivo = f'{nombre_archivo}.csv'
        ruta_destino = opciones.get('ruta_destino', '')
        ruta_archivo = f'{ruta_destino}/{nombre_archivo}'
        try:
            tabla = pd.read_html(io.StringIO(contenido), encoding='utf-8')[0]
            tabla.to_csv(
                ruta_archivo,
                header=True,
                index=False,
                encoding='utf-8',
                quoting=1
            )
            with open(ruta_archivo, 'rb') as f:
                csv_bytes = f.read()
                csv_io = io.BytesIO(csv_bytes)
            return csv_io
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error en ExportadorCsv',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO.HTTP_500_ERROR,
                detalles=[str(e)]
            )
