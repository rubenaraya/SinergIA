# pysinergia\conectores\disco_local.py

# --------------------------------------------------
# Importaciones de Infraestructura de Datos
import os, re
from pathlib import Path
from typing import BinaryIO

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.adaptadores import I_ConectorDisco as _Disco

# --------------------------------------------------
# Clase: DiscoLocal
# --------------------------------------------------
class DiscoLocal(_Disco):

    default_chunk_size = 64 * 1024
    _filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")

    def __init__(mi):
        mi.disco_ruta:str = None

    # --------------------------------------------------
    # Métodos privados

    def _secure_filename(mi, filename:str) -> str:
        """From Werkzeug secure_filename."""
        for sep in os.path.sep, os.path.altsep:
            if sep:
                filename = filename.replace(sep, ' ')
        normalized_filename = mi._filename_ascii_strip_re.sub("", "_".join(filename.split()))
        filename = str(normalized_filename).strip("._")
        return filename

    def _leer_nombre(mi, nombre:str) -> str:
        aux = Path(nombre).name
        return aux

    def _leer_ruta(mi, nombre:str) -> str:
        aux = str(mi._path / Path(nombre))
        return aux

    def _leer_peso(mi, nombre:str) -> int:
        aux = (mi._path / nombre).stat().st_size
        return aux

    # --------------------------------------------------
    # Métodos públicos

    def conectar(mi, config:dict) -> bool:
        disco_ruta = config.get('disco_ruta')
        mi._path = Path(disco_ruta)
        return True

    def generar_nombre(mi, nombre:str) -> str:
        counter = 0
        path = mi._path / mi._secure_filename(nombre)
        stem, extension = Path(nombre).stem, Path(nombre).suffix
        while path.exists():
            counter += 1
            path = mi._path / f"{stem}_{counter}{extension}"
        aux = path.name
        return aux

    def escribir(mi, archivo:BinaryIO, nombre:str) -> str:
        filename = mi._leer_nombre(nombre)
        path = mi._leer_ruta(filename)
        archivo.seek(0, 0)
        with open(path, "wb") as output:
            while True:
                chunk = archivo.read(mi.default_chunk_size)
                if not chunk:
                    break
                output.write(chunk)
        aux = str(path)
        return aux

    def abrir(mi, nombre:str) -> BinaryIO:
        path = mi._leer_ruta(nombre)
        aux = open(path, 'rb')
        return aux

    def eliminar(mi, nombre:str) -> bool:
        path = Path(mi._leer_ruta(nombre))
        aux = path.unlink()
        return aux

    def crear_carpeta(mi, nombre:str):
        path = Path(mi._leer_ruta(nombre))
        path.mkdir(parents=False, exist_ok=False)

    def eliminar_carpeta(mi, nombre:str):
        path = Path(mi._leer_ruta(nombre))
        path.rmdir()

    def comprobar_ruta(mi, nombre:str, tipo:str) -> bool:
        path = Path(mi._leer_ruta(nombre))
        aux = path.is_dir() if tipo == 'dir' else path.is_file()
        return aux

    # --------------------------------------------------

    def empaquetar_carpeta(mi, origen:str, destino:str):
        import zipfile
        return ''

    def extraer_carpeta(mi, origen:str, destino:str):
        import zipfile
        return ''

    def copiar(mi, origen:str, destino:str):
        return ''

    def mover(mi, origen:str, destino:str):
        return ''


# --------------------------------------------------
# Clase: Archivo (?)
# --------------------------------------------------
class Archivo:
    def __init__(mi):
        mi.ruta:str = ''
        mi.nombre:str = ''
        mi.ubicacion:str = ''
        mi.extension:str = ''
        mi.peso:int = 0
        mi.ancho:int = 0
        mi.alto:int = 0

