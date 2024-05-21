# pysinergia\exportadores\exportador_word.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador
from pysinergia.globales import Constantes as _Constantes

# --------------------------------------------------
# Clase: ExportadorWord
# --------------------------------------------------
class ExportadorWord(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str, opciones:dict={}):
        import subprocess, os, io
        dir_pandoc = os.path.normpath(os.path.abspath(_Constantes.DIR_LIB_PANDOC))
        """
        import pandoc
        os.environ["PATH"] = dir_pandoc + os.pathsep + os.getenv("PATH")
        pandoc.configure(path=dir_pandoc, version="3.2")
        doc = pandoc.read(contenido, format='html')
        res = pandoc.write(doc=doc, format='docx', file=destino)
        """
        ruta_pandoc = os.path.join(dir_pandoc,'pandoc')
        idioma = opciones.get('idioma', '')
        hoja_estilos = opciones.get('hoja_estilos', '')
        ruta_destino = opciones.get('ruta_destino', '')
        ruta_temp = mi.config.get('ruta_temp', '')
        dir_temp = f'{ruta_temp}/archivos'
        ruta_html = os.path.join(os.path.abspath(dir_temp),'temp.html')
        ruta_docx_temp = os.path.join(os.path.abspath(dir_temp),'temp.docx')
        with open(ruta_html, 'w') as f:
            f.write(contenido)
        salida_docx = ruta_destino if ruta_destino else ruta_docx_temp
        subprocess.run([ruta_pandoc, ruta_html, '-o', salida_docx])
        with open(salida_docx, 'rb') as f:
            docx_bytes = f.read()
            docx_io = io.BytesIO(docx_bytes)
        os.remove(ruta_html)
        if not ruta_destino:
            if os.path.exists(salida_docx):
                os.remove(salida_docx)
        return docx_io

