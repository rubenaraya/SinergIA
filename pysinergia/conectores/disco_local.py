# pysinergia\conectores\disco_local.py

# --------------------------------------------------
# Importaciones de Infraestructura de Datos
from pathlib import Path

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

    # --------------------------------------------------
    # Métodos privados

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
            nombre = mi.normalizar_nombre(mi._leer_nombre(nombre))
            path = (mi._path / nombre)
            base, extension = path.stem, path.suffix
            while path.exists():
                contador += 1
                path = (mi._path / f"{base}_{contador}{extension}")
            return path.name
        except Exception as e:
            print(e)

    def normalizar_nombre(mi, nombre:str, extension:str=None, largo:int=100, auto:bool=False) -> str:
        import re, unicodedata
        from uuid import uuid4
        if not nombre:
            if not auto:
                return ''
            nombre = str(uuid4())
        path = Path(nombre)
        extension_actual = path.suffix
        nombre_base = path.stem
        nombre_base = unicodedata.normalize('NFD', nombre_base).encode('ascii', 'ignore').decode('utf-8')
        nombre_base = re.sub(r"[ _]+", "-", nombre_base)
        nombre_base = re.sub(r'[\\/:"*?<>|°ºª~!#$%&=¿¡+{};@^`…(),\[\]\']', "", nombre_base)
        nombre_base = re.sub(r"-+", "-", nombre_base).strip("-")
        if extension:
            extension = f'.{extension.strip(".")}'
            if extension_actual and extension_actual.lower() != extension.lower():
                extension_actual = extension
            elif not extension_actual:
                extension_actual = extension
        else:
            extension_actual = extension_actual or ''
        nombre_normalizado = f"{nombre_base}{extension_actual}"
        if len(nombre_normalizado) > largo:
            recorte = largo - len(extension_actual)
            nombre_base = nombre_base[:recorte]
            nombre_normalizado = f"{nombre_base}{extension_actual}"
        return nombre_normalizado

    def eliminar(mi, nombre:str) -> bool:
        try:
            path = (mi._path / Path(nombre))
            if path.exists() and path.is_file:
                path.unlink()
                return True
        except Exception as e:
            print(e)
            return False

    def escribir(mi, contenido, nombre:str, modo:str='') -> str:
        try:
            ruta_archivo = mi._leer_ruta(nombre)
            modo_abrir = 'wb' if modo == 'b' else 'w'
            codificacion = None if modo == 'b' else 'utf-8'
            with open(ruta_archivo, mode=modo_abrir, encoding=codificacion) as archivo:
                if modo == 'b':
                    archivo.write(contenido.read())
                    contenido.seek(0)
                else:
                    archivo.write(contenido)
            return ruta_archivo
        except Exception as e:
            print(e)
            return None

    def abrir(mi, nombre:str, modo:str=''):
        try:
            ruta_archivo = mi._leer_ruta(nombre)
            modo_abrir = 'rb' if modo == 'b' else 'r'
            codificacion = None if modo == 'b' else 'utf-8'
            with open(ruta_archivo, mode=modo_abrir, encoding=codificacion) as archivo:
                return archivo.read()
        except Exception as e:
            print(e)
            return None

    def crear_carpeta(mi, nombre:str, antecesores:bool=False) -> str:
        try:
            path = (mi._path / Path(nombre))
            path.mkdir(parents=antecesores, exist_ok=True)
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

