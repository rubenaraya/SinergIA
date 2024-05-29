# pysinergia\exportadores\exportador_word.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import Exportador as _Exportador
from pysinergia import (
    Constantes as _Constantes,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorWord
# --------------------------------------------------
class ExportadorWord(_Exportador):

    def generar(mi, contenido:str, opciones:dict={}):
        import subprocess, os, io
        from uuid import uuid4
        uuid = str(uuid4())
        ruta_aux = mi.obtener_ruta()
        ruta_docx = f'{ruta_aux}/{uuid}.docx'
        ruta_html = f'{ruta_aux}/{uuid}.html'
        try:
            with open(ruta_html, 'w', encoding='utf-8') as f:
                f.write(contenido)
            dir_pandoc = os.path.normpath(os.path.abspath(_Constantes.DIR_LIB_PANDOC))
            ruta_pandoc = os.path.join(dir_pandoc,'pandoc')
            subprocess.run([ruta_pandoc, ruta_html, '-o', ruta_docx])
            os.remove(ruta_html)
            with open(ruta_docx, 'rb') as f:
                docx_bytes = f.read()
                docx_io = io.BytesIO(docx_bytes)
            os.remove(ruta_docx)
            return docx_io
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error-en-exportador-Word',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO._500_ERROR,
                detalles=[str(e)]
            )

