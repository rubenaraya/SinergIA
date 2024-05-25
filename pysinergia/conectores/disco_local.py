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

    def __init__(mi, config:dict):
        mi._config:dict = config or {}
        mi._path = Path(mi._config.get('ruta', ''))
        mi._longitud_fragmento = 64 * 1024
        mi._exp_nombre_ascii = re.compile(r"[^A-Za-z0-9_.-]")

    # --------------------------------------------------
    # Métodos privados

    def _normalizar_nombre(mi, nombre:str) -> str:
        """Werkzeug secure_filename."""
        for sep in os.path.sep, os.path.altsep:
            if sep:
                nombre = nombre.replace(sep, ' ')
        nombre_normalizado = mi._exp_nombre_ascii.sub('', '_'.join(nombre.split()))
        return str(nombre_normalizado).strip('._')

    def _leer_nombre(mi, nombre:str) -> str:
        return Path(nombre).name

    def _leer_ruta(mi, nombre:str) -> str:
        return str(mi._path / Path(nombre))

    def _leer_peso(mi, nombre:str) -> int:
        return (mi._path / Path(nombre)).stat().st_size

    # --------------------------------------------------
    # Métodos públicos

    def generar_nombre(mi, nombre:str) -> str:
        try:
            contador = 0
            nombre = mi._normalizar_nombre(mi._leer_nombre(nombre))
            path = (mi._path / nombre)
            base, extension = path.stem, path.suffix
            while path.exists():
                contador += 1
                path = (mi._path / f"{base}_{contador}{extension}")
            return path.name
        except Exception as e:
            print(e)

    def eliminar(mi, nombre:str) -> bool:
        try:
            path = (mi._path / Path(nombre))
            if path.exists() and path.is_file:
                path.unlink()
                return True
        except Exception as e:
            print(e)
            return False

    def escribir(mi, archivo:BinaryIO, nombre:str) -> str:
        try:
            ruta_archivo = mi._leer_ruta(nombre)
            archivo.seek(0, 0)
            with open(ruta_archivo, 'wb') as salida:
                while True:
                    fragmento = archivo.read(mi._longitud_fragmento)
                    if not fragmento:
                        break
                    salida.write(fragmento)
            return ruta_archivo
        except Exception as e:
            print(e)
            return None

    def abrir(mi, nombre:str) -> BinaryIO:
        try:
            ruta_archivo = mi._leer_ruta(nombre)
            with open(ruta_archivo, 'rb') as f:
                return f.read()
        except Exception as e:
            print(e)
            return None

    def crear_carpeta(mi, nombre:str) -> str:
        try:
            path = (mi._path / Path(nombre))
            path.mkdir(parents=True, exist_ok=True)
            if path.exists() and path.is_dir():
                return str(path.resolve())
            return ''
        except Exception as e:
            print(e)
            return ''

    def eliminar_carpeta(mi, nombre:str) -> bool:
        try:
            path = (mi._path / Path(nombre))
            if path.exists() and path.is_dir:
                path.rmdir()
                return True
        except Exception as e:
            print(e)
            return False

    def comprobar_ruta(mi, nombre:str, tipo:str='dir') -> bool:
        try:
            path = (mi._path / Path(nombre))
            resultado = path.is_dir() if tipo == 'dir' else path.is_file()
            if resultado is None:
                resultado = False
            return resultado
        except Exception as e:
            print(e)
            return False

