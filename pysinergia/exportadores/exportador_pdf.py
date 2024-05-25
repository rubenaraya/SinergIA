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
        import io, os
        try:
            hoja_estilos = opciones.get('hoja_estilos', '')
            ruta_plantillas = opciones.get('ruta_plantillas', '')
            if hoja_estilos and ruta_plantillas:
                if not os.path.exists(f'{ruta_plantillas}/{hoja_estilos}'):
                    ruta_plantillas = 'backend/plantillas'
                    if not os.path.exists(f'{ruta_plantillas}/{hoja_estilos}'):
                        hoja_estilos = ''
            css = CSS(filename=f'{ruta_plantillas}/{hoja_estilos}') if hoja_estilos else None
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

