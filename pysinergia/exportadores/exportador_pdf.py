# pysinergia\exportadores\exportador_pdf.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorPdf
# --------------------------------------------------
class ExportadorPdf(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str, opciones:dict={}, guardar:bool=False):
        from weasyprint import HTML, CSS
        import io, os
        ruta_destino = _Funciones.componer_ruta(opciones, 'pdf')
        hoja_estilos = _Funciones.comprobar_plantilla(opciones, 'hoja_estilos')
        try:
            css = CSS(filename=hoja_estilos) if hoja_estilos else None
            pdf = HTML(string=contenido).write_pdf(
                stylesheets=[css] if css else None,
            )
            if guardar and ruta_destino and pdf:
                if not os.path.exists(os.path.dirname(ruta_destino)):
                    os.makedirs(os.path.dirname(ruta_destino))
                with open(ruta_destino, 'wb') as f:
                    f.write(pdf)
            return io.BytesIO(pdf)
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error en ExportadorPdf',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO.HTTP_500_ERROR,
                detalles=[str(e)]
            )

