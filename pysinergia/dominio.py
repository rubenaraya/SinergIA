# pysinergia\dominio.py

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Dominio)
from typing import Dict, List, Optional, Self
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
    codigo: int | None = _Constantes.ESTADO._200_EXITO
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
    origen: object
    contenido: object = None
    nombre: Optional[str] = ''
    extension: Optional[str] = ''
    ruta: Optional[str] = ''
    carpeta: Optional[str] = ''
    tipo_mime: Optional[str] = ''
    peso: Optional[int] = 0
    es_valido: Optional[bool] = False
    mensaje_error: Optional[str] = ''

    RECHAZAR: str = 'RECHAZAR'
    SOBREESCRIBIR: str = 'SOBREESCRIBIR'
    RENOMBRAR: str = 'RENOMBRAR'

    def tipos_permitidos() -> List[str]:
        ...
    def peso_maximo() -> int:
        ...

    @model_validator(mode='after')
    def validar_archivo(cls, valores:Self):
        origen = valores.origen
        if not origen:
            valores.mensaje_error = 'No-se-recibio-ninguna-carga'
            return valores
        if origen.filename == '':
            valores.mensaje_error = 'La-carga-recibida-no-contiene-archivo'
            return valores
        valores.nombre = origen.filename
        valores.extension = valores.nombre.rsplit('.', 1)[1].lower()
        if origen.content_type not in cls.tipos_permitidos():
            valores.mensaje_error = 'El-tipo-de-archivo-no-esta-permitido'
            return valores
        valores.tipo_mime = origen.content_type
        valores.contenido = origen.file if hasattr(origen, 'file') else origen.stream
        valores.contenido.seek(0, 2)
        peso = valores.contenido.tell()
        valores.contenido.seek(0)
        valores.peso = peso
        if peso > cls.peso_maximo():
            valores.mensaje_error = 'El-archivo-supera-el-peso-maximo-aceptado'
            return valores
        valores.es_valido = True
        return valores

# --------------------------------------------------
# ClaseModelo: CargaImagen
# --------------------------------------------------
class CargaImagen(CargaArchivo):
    carpeta: Optional[str] = 'imagenes'
    ancho: Optional[int] = 0
    altura: Optional[int] = 0

    def tipos_permitidos() -> List[str]:
        return [
            _Constantes.MIME.JPG,
            _Constantes.MIME.JPEG,
            _Constantes.MIME.PNG,
        ]
    def peso_maximo() -> int:
        return 5 * 1024 * 1024

# --------------------------------------------------
# ClaseModelo: CargaDocumento
# --------------------------------------------------
class CargaDocumento(CargaArchivo):
    carpeta: Optional[str] = 'documentos'

    def tipos_permitidos() -> List[str]:
        return [
            _Constantes.MIME.DOCX,
            _Constantes.MIME.DOC,
            _Constantes.MIME.XLSX,
            _Constantes.MIME.XLS,
            _Constantes.MIME.PPTX,
            _Constantes.MIME.PPT,
            _Constantes.MIME.PDF,
            _Constantes.MIME.CSV,
        ]
    def peso_maximo() -> int:
        return 2 * 1024 * 1024

# --------------------------------------------------
# ClaseModelo: CargaAudio
# --------------------------------------------------
class CargaAudio(CargaArchivo):
    carpeta: Optional[str] = 'audios'

    def tipos_permitidos() -> List[str]:
        return [
            _Constantes.MIME.MP3,
            _Constantes.MIME.WAV,
            _Constantes.MIME.OGG,
            _Constantes.MIME.OPUS,
            _Constantes.MIME.WMA,
            _Constantes.MIME.WEBA,
        ]
    def peso_maximo() -> int:
        return 25 * 1024 * 1024

# --------------------------------------------------
# ClaseModelo: CargaVideo
# --------------------------------------------------
class CargaVideo(CargaArchivo):
    carpeta: Optional[str] = 'videos'
    def tipos_permitidos() -> List[str]:
        return [
            _Constantes.MIME.MP4,
            _Constantes.MIME.WEBM,
            _Constantes.MIME.WMV,
        ]
    def peso_maximo() -> int:
        return 25 * 1024 * 1024


# --------------------------------------------------
# ClaseModelo: Archivo
# --------------------------------------------------
class Archivo(BaseModel):
    nombre: Optional[str] = ''
    ruta: Optional[str] = ''
    ubicacion: Optional[str] = ''
    base: Optional[str] = ''
    extension: Optional[str] = ''
    peso: Optional[int] = 0
