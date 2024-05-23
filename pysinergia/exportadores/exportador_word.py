# pysinergia\exportadores\exportador_word.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
    ErrorPersonalizado as _ErrorPersonalizado,
)

# --------------------------------------------------
# Clase: ExportadorWord
# --------------------------------------------------
class ExportadorWord(_I_Exportador):
    def __init__(mi, config:dict={}):
        mi.config:dict = config

    def generar(mi, contenido:str, opciones:dict={}, guardar:bool=False):
        import subprocess, os, io, shutil
        from uuid import uuid4
        uuid = str(uuid4())
        ruta_destino = _Funciones.componer_ruta(opciones, 'docx')
        ruta_temp = mi.config.get('ruta_temp', '')
        ruta_aux = os.path.abspath(f'{ruta_temp}/archivos')
        ruta_docx = os.path.join(ruta_aux, f'{uuid}.docx')
        ruta_html = os.path.join(ruta_aux, f'{uuid}.html')
        try:
            with open(ruta_html, 'w', encoding='utf-8') as f:
                f.write(contenido)
            dir_pandoc = os.path.normpath(os.path.abspath(_Constantes.DIR_LIB_PANDOC))
            ruta_pandoc = os.path.join(dir_pandoc,'pandoc')
            os.environ["PATH"] = dir_pandoc + os.pathsep + os.getenv("PATH")
            subprocess.run([ruta_pandoc, ruta_html, '-o', ruta_docx])
            os.remove(ruta_html)
            with open(ruta_docx, 'rb') as f:
                docx_bytes = f.read()
                docx_io = io.BytesIO(docx_bytes)
            if ruta_destino and guardar:
                if not os.path.exists(os.path.dirname(ruta_destino)):
                    os.makedirs(os.path.dirname(ruta_destino))
                shutil.move(ruta_docx, ruta_destino)
            else:
                os.remove(ruta_docx)
            return docx_io
        except Exception as e:
            raise _ErrorPersonalizado(
                mensaje='Error en ExportadorWord',
                tipo=_Constantes.SALIDA.ERROR,
                codigo=_Constantes.ESTADO.HTTP_500_ERROR,
                detalles=[str(e)]
            )

