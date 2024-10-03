# --------------------------------------------------
# pysinergia\complementos\exportador_word.py
# --------------------------------------------------

# Importaciones de PySinergIA
from pysinergia.complementos.exportador import (
    Exportador,
    ErrorExportador,
)
from pysinergia import Constantes

# --------------------------------------------------
# Clase: ExportadorWord
class ExportadorWord(Exportador):

    def generar(mi, contenido:str, opciones:dict={}):
        import subprocess, io, os
        from pathlib import Path
        from uuid import uuid4
        uuid = str(uuid4())
        ruta_aux = Path(mi.obtener_ruta())
        ruta_html = ruta_aux / f'{uuid}.html'
        ruta_docx = ruta_aux / f'{uuid}.docx'
        try:
            ruta_html.write_text(contenido, encoding='utf-8')
            dir_pandoc = Path(os.getenv('RUTA_LIB_PANDOC')).resolve()
            ruta_pandoc = dir_pandoc / 'pandoc'
            if ruta_pandoc.is_file():
                subprocess.run([str(ruta_pandoc), str(ruta_html), '-o', str(ruta_docx)])
                docx_bytes = ruta_docx.read_bytes()
                ruta_html.unlink()
                ruta_docx.unlink()
                docx_io = io.BytesIO(docx_bytes)
                return docx_io
            return None
        except Exception as e:
            raise ErrorExportador(
                mensaje='Error-en-exportador-Word',
                codigo=Constantes.ESTADO._500_ERROR,
                tipo=type(e).__name__,
            )

