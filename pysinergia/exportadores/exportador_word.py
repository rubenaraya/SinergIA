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
        dir_pandoc = os.path.normpath(os.path.abspath(_Constantes.DIR_LIB_PANDOC))
        """
        import pandoc
        os.environ["PATH"] = dir_pandoc + os.pathsep + os.getenv("PATH")
        config = pandoc.configure(path=dir_pandoc, version="3.2.0", read=True)
        doc = pandoc.read(contenido, format='html')
        res = pandoc.write(doc=doc, format='docx', file=destino)
        """
        ruta_pandoc = os.path.join(dir_pandoc,'pandoc')
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
            if os.path.exists(salida_docx):
                os.remove(salida_docx)
        return docx_io

