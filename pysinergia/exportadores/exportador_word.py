# pysinergia\exportadores\exportador_word.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador
from pysinergia.globales import Constantes as _Constantes

# --------------------------------------------------
# Clase: ExportadorWord
# --------------------------------------------------
class ExportadorWord(_I_Exportador):
    def __init__(mi, opciones:dict={}):
        mi.opciones:dict = opciones

    def generar(mi, contenido:str, destino:str=''):
        import subprocess, os, io
        ruta_pandoc = os.path.join(os.path.abspath(_Constantes.DIR_LIB_PANDOC),'pandoc')
        ruta_temp = str(mi.opciones.get('ruta_temp', ''))
        dir_temp = f'{ruta_temp}/archivos'
        idioma = mi.opciones.get('idioma')
        ruta_html = os.path.join(os.path.abspath(dir_temp),'temp.html')
        ruta_docx_temp = os.path.join(os.path.abspath(dir_temp),'temp.docx')
        with open(ruta_html, 'w') as f:
            f.write(contenido)
        salida_docx = destino if destino else ruta_docx_temp
        subprocess.run([ruta_pandoc, ruta_html, '-o', salida_docx])
        with open(salida_docx, 'rb') as f:
            docx_bytes = f.read()
            docx_io = io.BytesIO(docx_bytes)
        os.remove(ruta_html)
        if not destino:
            os.remove(salida_docx)
        return docx_io

