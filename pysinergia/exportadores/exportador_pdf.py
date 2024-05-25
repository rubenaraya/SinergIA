# pysinergia\exportadores\exportador_pdf.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import Exportador as _Exportador
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorPdf
# --------------------------------------------------
class ExportadorPdf(_Exportador):

    def generar(mi, contenido:str, opciones:dict={}):
        from weasyprint import HTML, CSS
        import io
        hoja_estilos, ruta_hoja_estilos = _Funciones.comprobar_plantilla(opciones, 'hoja_estilos')
        try:
            css = CSS(filename=f'{ruta_hoja_estilos}/{hoja_estilos}') if hoja_estilos else None
            pdf = HTML(string=contenido).write_pdf(
                stylesheets=[css] if css else None,
            )
            return io.BytesIO(pdf)
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error en ExportadorPdf',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO.HTTP_500_ERROR,
                detalles=[str(e)]
            )

