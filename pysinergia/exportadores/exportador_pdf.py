# pysinergia\exportadores\exportador_pdf.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import Exportador as _Exportador
from pysinergia import (
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorPdf
# --------------------------------------------------
class ExportadorPdf(_Exportador):

    def generar(mi, contenido:str, opciones:dict={}):
        from weasyprint import HTML, CSS
        from pathlib import Path
        import io
        try:
            hoja_estilos = str(opciones.get('hoja_estilos', ''))
            ruta_plantillas = Path(opciones.get('ruta_plantillas', ''))
            if hoja_estilos:
                ruta_css = (ruta_plantillas / hoja_estilos)
                if not ruta_css.exists():
                    ruta_plantillas = Path('backend/plantillas')
                    ruta_css = ruta_plantillas / hoja_estilos
                    if not ruta_css.exists():
                        hoja_estilos = ''
            css = CSS(filename=str(ruta_css)) if hoja_estilos else None
            pdf = HTML(string=contenido).write_pdf(stylesheets=[css] if css else None)
            return io.BytesIO(pdf)
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error-en-exportador-PDF',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO._500_ERROR,
                detalles=[str(e)]
            )

