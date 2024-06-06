# pysinergia\conectores\disco_local.py

from pathlib import Path
from typing import (BinaryIO, TextIO, List)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.dominio import Archivo as _Archivo
from pysinergia.conectores.disco import (
    Disco as _Disco,
    ErrorDisco as _ErrorDisco,
)

# --------------------------------------------------
# Clase: DiscoLocal
# --------------------------------------------------
class DiscoLocal(_Disco):

    def __init__(mi, config:dict):
        super().__init__(config)
        mi._path = Path(mi._config.get('ruta', ''))

    # --------------------------------------------------
    # Métodos privados

    def _leer_nombre(mi, nombre:str) -> str:
        return Path(nombre).name

    def _leer_ruta(mi, nombre:str) -> str:
        return (mi._path / Path(nombre)).as_posix()

    def _leer_peso(mi, nombre:str) -> int:
        return (mi._path / Path(nombre)).stat().st_size

    # --------------------------------------------------
    # Métodos públicos

    def generar_nombre(mi, nombre:str, unico:bool=False) -> str:
        path = (mi._path / mi.normalizar_nombre(nombre))
        if unico and path.exists():
            base, extension = path.stem, path.suffix
            contador = 1
            while (mi._path / f"{base}_{contador}{extension}").exists():
                contador += 1
            return f"{base}_{contador}{extension}"
        return path.name

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
        nombre_base = re.sub(r'[\\/:"*?<>|°ºª~!#$%&=¿¡+{};@^`…(),\.\[\]\']', "", nombre_base)
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
            else:
                return False
        except FileNotFoundError as e:
            raise _ErrorDisco(mensaje='Archivo-no-encontrado', ruta=nombre, detalles=[str(e)])
        except PermissionError as e:
            raise _ErrorDisco(mensaje='Permiso-denegado-para-eliminar-el-archivo', ruta=nombre, detalles=[str(e)])
        except Exception as e:
            raise _ErrorDisco(mensaje='Error-desconocido-al-acceder-al-archivo', ruta=nombre, detalles=[str(e)])

    def escribir(mi, contenido: BinaryIO | TextIO, nombre:str, modo:str='') -> str:
        ruta_archivo = mi._leer_ruta(nombre)
        modo_abrir = 'wb' if 'b' in modo else 'w'
        codificacion = None if 'b' in modo else 'utf-8'
        try:
            with open(ruta_archivo, mode=modo_abrir, encoding=codificacion) as archivo:
                if modo == 'b':
                    while fragmento := contenido.read(1024 * 1024):
                        archivo.write(fragmento)
                    contenido.seek(0)
                else:
                    archivo.write(contenido)
            return ruta_archivo
        except PermissionError as e:
            raise _ErrorDisco(mensaje='Permiso-denegado-para-escribir-el-archivo', ruta=nombre, detalles=[str(e)])
        except IOError as e:
            raise _ErrorDisco(mensaje='Error-de-IO-al-escribir-el-archivo', ruta=nombre, detalles=[str(e)])
        except Exception as e:
            raise _ErrorDisco(mensaje='Error-desconocido-al-acceder-al-archivo', ruta=nombre, detalles=[str(e)])
        finally:
            if archivo:
                archivo.close()

    def abrir(mi, nombre:str, modo:str='') -> BinaryIO | TextIO:
        ruta_archivo = mi._leer_ruta(nombre)
        modo_abrir = 'rb' if 'b' in modo else 'r'
        codificacion = None if 'b' in modo else 'utf-8'
        try:
            with open(ruta_archivo, mode=modo_abrir, encoding=codificacion) as archivo:
                return archivo.read()
        except FileNotFoundError as e:
            raise _ErrorDisco(mensaje='Archivo-no-encontrado', ruta=nombre, detalles=[str(e)])
        except PermissionError as e:
            raise _ErrorDisco(mensaje='Permiso-denegado-para-abrir-el-archivo', ruta=nombre, detalles=[str(e)])
        except Exception as e:
            raise _ErrorDisco(mensaje='Error-desconocido-al-acceder-al-archivo', ruta=nombre, detalles=[str(e)])

    def copiar(mi, nombre:str, dir_destino:str, mover:bool=False) -> bool:
        import shutil
        try:
            ruta_archivo_path = (mi._path / Path(nombre))
            dir_destino_path = (mi._path / Path(dir_destino))
            if not ruta_archivo_path.is_file():
                return False
            dir_destino_path.mkdir(parents=True, exist_ok=True)
            archivo_destino_path = (dir_destino_path / ruta_archivo_path.name)
            if mover:
                shutil.move(str(ruta_archivo_path), str(archivo_destino_path))
            else:
                shutil.copy(str(ruta_archivo_path), str(archivo_destino_path))
            return True
        except Exception as e:
            print(e)
            return False

    def crear_carpeta(mi, nombre:str, antecesores:bool=False) -> str:
        try:
            path = (mi._path / Path(nombre))
            path.mkdir(parents=antecesores, exist_ok=True)
            if path.exists() and path.is_dir():
                return str(path.resolve().as_posix())
            return ''
        except PermissionError as e:
            raise _ErrorDisco(mensaje='Permiso-denegado-para-crear-la-carpeta', ruta=nombre, detalles=[str(e)])
        except OSError as e:
            raise _ErrorDisco(mensaje='Error-del-sistema-operativo-al-crear-la-carpeta', ruta=nombre, detalles=[str(e)])
        except Exception as e:
            raise _ErrorDisco(mensaje='Error-desconocido-al-acceder-a-la-carpeta', ruta=nombre, detalles=[str(e)])

    def eliminar_carpeta(mi, nombre:str) -> bool:
        try:
            path = (mi._path / Path(nombre))
            if path.exists() and path.is_dir:
                path.rmdir()
                return True
            else:
                raise _ErrorDisco(mensaje='La-carpeta-no-existe', ruta=nombre)
        except PermissionError as e:
            raise _ErrorDisco(mensaje='Permiso-denegado-para-eliminar-la-carpeta', ruta=nombre, detalles=[str(e)])
        except OSError as e:
            raise _ErrorDisco(mensaje='Error-del-sistema-operativo-al-eliminar-la-carpeta', ruta=nombre, detalles=[str(e)])
        except Exception as e:
            raise _ErrorDisco(mensaje='Error-desconocido-al-acceder-a-la-carpeta', ruta=nombre, detalles=[str(e)])

    def comprobar_ruta(mi, nombre:str, tipo:str='') -> str:
        path = (mi._path / Path(nombre))
        resultado = path.is_dir() if tipo == 'dir' else path.is_file()
        if resultado:
            return path.as_posix()
        return None

    def listar_archivos(mi, nombre:str, extension:str='*') -> List[_Archivo]:
        lista = []
        path = (mi._path / Path(nombre))
        if path.exists() and path.is_dir():
            for archivo in path.rglob(f'*.{extension}'):
                if archivo.is_file:
                    lista.append(_Archivo(
                        nombre=archivo.name,
                        ruta=archivo.as_posix(),
                        ubicacion=archivo.parent.as_posix(),
                        base=archivo.stem,
                        extension=str(archivo.suffix).strip('.'),
                        peso=archivo.stat().st_size
                    ))
        return lista

    def empaquetar_zip(mi, dir_origen:str, ruta_archivo_zip:str) -> bool:
        from zipfile import ZipFile, ZIP_DEFLATED
        try:
            dir_origen_path = (mi._path / Path(dir_origen))
            ruta_archivo_zip_path = (mi._path / Path(ruta_archivo_zip))
            with ZipFile(ruta_archivo_zip_path, 'w', ZIP_DEFLATED) as zipf:
                for archivo in dir_origen_path.rglob('*'):
                    if archivo.is_file():
                        ruta_relativa = archivo.relative_to(dir_origen_path)
                        zipf.write(archivo, ruta_relativa)
            return True
        except Exception as e:
            print(e)
            return False

    def extraer_zip(mi, ruta_archivo_zip:str, dir_destino:str) -> bool:
        from zipfile import ZipFile
        try:
            ruta_archivo_zip_path = (mi._path / Path(ruta_archivo_zip))
            dir_destino_path = (mi._path / Path(dir_destino))
            dir_destino_path.mkdir(parents=True, exist_ok=True)
            with ZipFile(ruta_archivo_zip_path, 'r') as zipf:
                zipf.extractall(dir_destino_path)
            return True
        except Exception as e:
            print(e)
            return False

    def convertir_imagen(mi, ruta_imagen:str, dir_destino:str, lista_salidas:list[dict]) -> list[str]:
        from PIL import Image
        try:
            ruta_imagen_path = (mi._path / Path(ruta_imagen))
            dir_destino_path = (mi._path / Path(dir_destino))
            dir_destino_path.mkdir(parents=True, exist_ok=True)
            resultado:list = []
            with Image.open(ruta_imagen_path) as img:
                for salida in lista_salidas:
                    try:
                        ancho = salida.get('ancho')
                        alto = salida.get('alto')
                        formato = salida.get('formato')
                        nombre = salida.get('nombre')
                        ruta_salida = (dir_destino_path / Path(nombre))
                        imagen = img.resize((ancho, alto), Image.Resampling.LANCZOS)
                        imagen.save(ruta_salida, format=formato)
                        resultado.append(ruta_salida.as_posix())
                    except Exception as e:
                        print(e)
            return resultado
        except Exception as e:
            print(e)
            return []

