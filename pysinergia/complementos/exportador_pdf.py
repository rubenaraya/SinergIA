# pysinergia\complementos\exportador_pdf.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.complementos.exportador import (
    Exportador as _Exportador,
    ErrorExportador as _ErrorExportador,
)
from pysinergia import (
    Constantes as _Constantes,
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
            raise _ErrorExportador(
                mensaje='Error-en-exportador-PDF',
                codigo=_Constantes.ESTADO._500_ERROR,
                detalles=[str(e)]
            )

