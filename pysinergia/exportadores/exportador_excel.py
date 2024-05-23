# pysinergia\exportadores\exportador_excel.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorExcel
# --------------------------------------------------
class ExportadorExcel(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str, opciones:dict={}, guardar:bool=False):
        import pandas as pd
        import io, os, shutil
        from uuid import uuid4
        uuid = str(uuid4())
        tabla_datos = opciones.get('tabla_datos', 'Hoja1')
        ruta_destino = _Funciones.componer_ruta(opciones, 'xlsx')
        ruta_temp = mi.config.get('ruta_temp', '')
        ruta_xlsx = os.path.join(os.path.abspath(f'{ruta_temp}/archivos'), f'{uuid}.xlsx')
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
            if ruta_destino and guardar:
                if not os.path.exists(os.path.dirname(ruta_destino)):
                    os.makedirs(os.path.dirname(ruta_destino))
                shutil.move(ruta_xlsx, ruta_destino)
            else:
                os.remove(ruta_xlsx)
            return xlsx_io
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error en ExportadorExcel',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO.HTTP_500_ERROR,
                detalles=[str(e)]
            )

