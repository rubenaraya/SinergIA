# --------------------------------------------------
# pysinergia\complementos\exportador_pdf.py
# --------------------------------------------------

# Importaciones de PySinergIA
from pysinergia.complementos.exportador import (
    Exportador,
    ErrorExportador,
)
from pysinergia.globales import Constantes

# --------------------------------------------------
# Clase: ExportadorPdf
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class ExportadorPdf(Exportador):

    def generar(mi, contenido:str, opciones:dict={}):
        from weasyprint import HTML, CSS
        from pathlib import Path
        import io
        try:
            hoja_estilos = str(opciones.get('hoja_estilos', ''))
            ruta_plantillas = opciones.get('ruta_plantillas', '')
            if hoja_estilos:
                ruta_css = (Path(ruta_plantillas) / hoja_estilos)
                if not ruta_css.exists():
                    ruta_plantillas = mi.config_web.get('RUTA_PLANTILLAS')
                    ruta_css = (Path(ruta_plantillas) / hoja_estilos)
                    if not ruta_css.exists():
                        hoja_estilos = ''
            css = CSS(filename=str(ruta_css)) if hoja_estilos else None
            pdf = HTML(string=contenido).write_pdf(stylesheets=[css] if css else None)
            return io.BytesIO(pdf)
        except Exception as e:
            raise ErrorExportador(
                mensaje='Error-en-exportador-PDF',
                codigo=Constantes.ESTADO._500_ERROR,
                tipo=type(e).__name__,
            )

