# pysinergia\exportadores\exportador_pdf.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador

# --------------------------------------------------
# Clase: ExportadorPdf
# --------------------------------------------------
class ExportadorPdf(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str, opciones:dict={}):
        from weasyprint import HTML, CSS
        import io
        nombre_archivo = opciones.get('nombre_archivo', '')
        if nombre_archivo and not str(nombre_archivo).endswith('.pdf'):
            nombre_archivo = f'{nombre_archivo}.pdf'
        ruta_destino = opciones.get('ruta_destino', '')
        ruta_archivo = f'{ruta_destino}/{nombre_archivo}'
        hoja_estilos = opciones.get('hoja_estilos', '')
        css = CSS(filename=hoja_estilos) if hoja_estilos else None
        pdf = HTML(string=contenido).write_pdf(
            stylesheets=[css] if css else None,
        )
        if ruta_destino and nombre_archivo and pdf:
            with open(ruta_archivo, 'wb') as f:
                f.write(pdf)
        return io.BytesIO(pdf)

