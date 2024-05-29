# pysinergia\dominio.py

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Dominio)
from typing import Dict, Optional
from pydantic import BaseModel, model_validator

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
)

# --------------------------------------------------
# Clase: Entidad
# --------------------------------------------------
class Entidad:
    ...


# --------------------------------------------------
# ClaseModelo: ModeloPeticion
# --------------------------------------------------
class ModeloPeticion(BaseModel):

    def diccionario(mi) -> Dict:
        return mi.model_dump()

    def json(mi) -> str:
        return mi.model_dump_json()


# --------------------------------------------------
# ClaseModelo: ModeloRespuesta
# --------------------------------------------------
class ModeloRespuesta(BaseModel):

    def diccionario(mi) -> Dict:
        return mi.model_dump()

    def json(mi) -> str:
        return mi.model_dump_json()


# --------------------------------------------------
# ClaseModelo: RespuestaResultado
# --------------------------------------------------
class RespuestaResultado(ModeloRespuesta):
    codigo: int | None = _Constantes.ESTADO.HTTP_200_EXITO
    tipo: str | None = _Constantes.SALIDA.EXITO
    mensaje: str | None = ''
    resultado: dict | None = {}
    esquemas: dict | None = {}
    opciones: dict | None = {}

    def asignar_contexto(mi, estado:int, mensaje:str=''):
        mi.codigo = estado
        mi.tipo = _Funciones.tipo_salida(estado)
        if mensaje:
            mi.mensaje = mensaje


# --------------------------------------------------
# ClaseModelo: CargaArchivo
# --------------------------------------------------
class CargaArchivo(BaseModel):
    carga: Optional[object]
    nombre: Optional[str]
    tipo_mime: Optional[str]
    peso: Optional[int] | None = 0
    validacion: Optional[bool] | None = False
    mensaje_error: Optional[str] | None = ''

    class Config:
        arbitrary_types_allowed = True
    def tipos_permitidos() -> list:
        ...
    def peso_maximo() -> int:
        ...

    @model_validator(mode='after')
    def validar_archivo(cls, valores):
        carga = valores.carga
        if not carga:
            valores.mensaje_error = 'No-se-recibio-carga'
            return valores
        nombre = valores.nombre
        if nombre == '':
            valores.mensaje_error = 'La-carga-no-contiene-archivos'
            return valores
        tipo_mime = valores.tipo_mime
        if tipo_mime not in cls.tipos_permitidos():
            valores.mensaje_error = 'Tipo-de-archivo-no-permitido'
            return valores
        carga.seek(0, 2)
        peso = carga.tell()
        carga.seek(0)
        valores.peso = peso
        if peso > cls.peso_maximo():
            valores.mensaje_error = 'El-archivo-supera-el-peso-maximo'
            return valores
        valores.validacion = True
        return valores

# --------------------------------------------------
# ClaseModelo: CargaImagen
# --------------------------------------------------
class CargaImagen(CargaArchivo):
    def tipos_permitidos() -> list:
        return [
            _Constantes.MIME.JPG,
            _Constantes.MIME.PNG,
        ]
    def peso_maximo() -> int:
        return 5 * 1024 * 1024

# --------------------------------------------------
# ClaseModelo: CargaDocumento
# --------------------------------------------------
class CargaDocumento(CargaArchivo):
    def tipos_permitidos() -> list:
        return [
            _Constantes.MIME.DOCX,
            _Constantes.MIME.XLSX,
            _Constantes.MIME.PPTX,
            _Constantes.MIME.PDF,
        ]
    def peso_maximo() -> int:
        return 2 * 1024 * 1024

# --------------------------------------------------
# ClaseModelo: CargaAudio
# --------------------------------------------------
class CargaAudio(CargaArchivo):
    def tipos_permitidos() -> list:
        return [
            _Constantes.MIME.MP3,
            _Constantes.MIME.WAV,
            _Constantes.MIME.OPUS,
            _Constantes.MIME.WEBA,
        ]
    def peso_maximo() -> int:
        return 25 * 1024 * 1024

# --------------------------------------------------
# ClaseModelo: CargaVideo
# --------------------------------------------------
class CargaVideo(CargaArchivo):
    def tipos_permitidos() -> list:
        return [
            _Constantes.MIME.MP4,
            _Constantes.MIME.WEBM,
        ]
    def peso_maximo() -> int:
        return 25 * 1024 * 1024

