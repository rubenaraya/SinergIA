# pysinergia\exportadores\exportador_word.py

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_Exportador as _I_Exportador

# --------------------------------------------------
# Clase: ExportadorWord
# --------------------------------------------------
class ExportadorWord(_I_Exportador):
    def __init__(mi, opciones:dict={}):
        mi.opciones:dict = opciones

    def generar(mi, contenido:str, destino:str=''):
        import pandoc, io, subprocess

        ruta_html = './tmp/prueba/archivos/temp.html'
        with open(ruta_html, 'w') as html_file:
            html_file.write(contenido)

        if destino:
            subprocess.run(["./_lib/pandoc/pandoc", ruta_html, "-o", destino])
