# pysinergia\exportadores\exportador_csv.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorCsv
# --------------------------------------------------
class ExportadorCsv(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str='', opciones:dict={}, guardar:bool=False):
        import pandas as pd
        import io, os, shutil
        from uuid import uuid4
        uuid = str(uuid4())
        ruta_destino = _Funciones.componer_ruta(opciones, 'csv')
        ruta_temp = mi.config.get('ruta_temp', '')
        ruta_csv = os.path.join(os.path.abspath(f'{ruta_temp}/archivos'), f'{uuid}.csv')
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
            if ruta_destino and guardar:
                if not os.path.exists(os.path.dirname(ruta_destino)):
                    os.makedirs(os.path.dirname(ruta_destino))
                shutil.move(ruta_csv, ruta_destino)
            else:
                os.remove(ruta_csv)
            return csv_io
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error en ExportadorCsv',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO.HTTP_500_ERROR,
                detalles=[str(e)]
            )

