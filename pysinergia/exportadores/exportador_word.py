# pysinergia\exportadores\exportador_word.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.exportadores.exportador import (
    Exportador as _Exportador,
    ErrorExportador as _ErrorExportador,
)
from pysinergia import (
    Constantes as _Constantes,
)

# --------------------------------------------------
# Clase: ExportadorWord
# --------------------------------------------------
class ExportadorWord(_Exportador):

    def generar(mi, contenido:str, opciones:dict={}):
        import subprocess, io
        from pathlib import Path
        from uuid import uuid4
        uuid = str(uuid4())
        ruta_aux = Path(mi.obtener_ruta())
        ruta_html = ruta_aux / f'{uuid}.html'
        ruta_docx = ruta_aux / f'{uuid}.docx'
        try:
            ruta_html.write_text(contenido, encoding='utf-8')
            dir_pandoc = Path(_Constantes.DIR_LIB_PANDOC).resolve()
            ruta_pandoc = dir_pandoc / 'pandoc'
            subprocess.run([str(ruta_pandoc), str(ruta_html), '-o', str(ruta_docx)])
            docx_bytes = ruta_docx.read_bytes()
            ruta_html.unlink()
            ruta_docx.unlink()
            docx_io = io.BytesIO(docx_bytes)
            return docx_io
        except Exception as e:
            raise _ErrorExportador(
                mensaje='Error-en-exportador-Word',
                codigo=_Constantes.ESTADO._500_ERROR,
                detalles=[str(e)]
            )
