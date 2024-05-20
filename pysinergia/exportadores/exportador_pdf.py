# pysinergia\exportadores\exportador_pdf.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador

# --------------------------------------------------
# Clase: ExportadorPdf
# --------------------------------------------------
class ExportadorPdf(_I_Exportador):
    def __init__(mi, opciones:dict={}):
        mi.opciones:dict = opciones

    def generar(mi, contenido:str, destino:str=''):
        from weasyprint import HTML, CSS
        import io
        estilos_css = mi.opciones.get('estilos_css', '')
        css = CSS(filename=estilos_css) if estilos_css else None
        pdf = HTML(string=contenido).write_pdf(stylesheets=[css] if css else None)
        if destino:
            with open(destino, 'wb') as f:
                f.write(pdf)
        return io.BytesIO(pdf)

