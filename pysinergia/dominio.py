# pysinergia\dominio.py

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Dominio)
from typing import (
    Dict,
    List,
    Optional,
    Self,
    Tuple,
    Any,
    Literal,
)
from enum import Enum
from pydantic import (
    BaseModel,
    ConfigDict,
    create_model,
    model_validator,
    field_validator,
    Field,
)
import gettext

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import (
    Constantes as _Constantes,
    Funciones as _Funciones,
    Traductor as _Traductor,
)

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
    model_config = ConfigDict(arbitrary_types_allowed=True)

    T:_Traductor | None = None
    codigo: int | None = _Constantes.ESTADO._200_EXITO
    tipo:str | None = _Constantes.SALIDA.EXITO
    mensaje:str | None = ''
    titulo:str = ''
    descripcion:str = ''
    fecha_actual:str = ''
    hora_actual:str = ''
    idioma:str = ''
    detalles: list = []
    resultado: dict | None = {}
    opciones: dict | None = {}
    fecha: dict | None = {}

    @model_validator(mode='after')
    def model_validator(cls, valores:Self) -> 'ModeloRespuesta':
        if valores.T:
            from collections import ChainMap
            fechahora = valores.T.fecha_hora()
            valores.fecha_actual = fechahora.get('fecha')
            valores.hora_actual = fechahora.get('hora')
            valores.idioma = valores.T.idioma
            _:gettext.GNUTranslations = valores.T.abrir_traduccion()
            datos = ChainMap(cls._filtrar_diccionario(valores.resultado), valores.opciones, valores.fecha)
            valores.mensaje = str(_(valores.mensaje)).format(**datos) if valores.mensaje else ''
            valores.titulo = str(_(valores.titulo)).format(**datos) if valores.titulo else ''
            valores.descripcion = str(_(valores.descripcion)).format(**datos) if valores.descripcion else ''
        return valores

    def _filtrar_diccionario(diccionario:dict):
        return {k: v for k, v in diccionario.items() if isinstance(v, (str, int, float, bool))}

    def diccionario(mi) -> Dict:
        mi.T = None
        diccionario = mi.model_dump()
        diccionario.pop('T')
        return diccionario

    def json(mi) -> str:
        mi.T = None
        return mi.model_dump_json()

    def asignar_datos(mi, codigo:int=None, mensaje:str=None, titulo:str=None, descripcion:str=None):
        if codigo:
            mi.codigo = codigo
            mi.tipo = _Funciones.tipo_salida(codigo)
        if mensaje:
            mi.mensaje = mensaje
        if titulo:
            mi.titulo = titulo
        if descripcion:
            mi.descripcion = descripcion

# --------------------------------------------------
# ClaseModelo: RespuestaResultado
# --------------------------------------------------
class RespuestaResultado(ModeloRespuesta):
    esquemas: dict | None = {}


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
    codigo: Optional[int] = _Constantes.ESTADO._200_EXITO
    resultado: Optional[str] = _Constantes.SALIDA.EXITO
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
    def validate_model(cls, valores:Self) -> 'CargaArchivo':
        origen = valores.origen
        if not origen:
            valores.mensaje_error = 'No-se-recibio-ninguna-carga'
            valores.codigo = _Constantes.ESTADO._422_NO_PROCESABLE
            valores.resultado = _Constantes.SALIDA.ALERTA
            return valores
        if origen.filename == '':
            valores.mensaje_error = 'La-carga-recibida-no-contiene-archivo'
            valores.codigo = _Constantes.ESTADO._400_NO_VALIDO
            valores.resultado = _Constantes.SALIDA.ALERTA
            return valores
        valores.nombre = origen.filename
        valores.extension = valores.nombre.rsplit('.', 1)[1].lower()
        if origen.content_type not in cls.tipos_permitidos():
            valores.mensaje_error = 'El-tipo-de-archivo-no-esta-permitido'
            valores.codigo = _Constantes.ESTADO._415_NO_SOPORTADO
            valores.resultado = _Constantes.SALIDA.ALERTA
            return valores
        valores.tipo_mime = origen.content_type
        valores.contenido = origen.file if hasattr(origen, 'file') else origen.stream
        valores.contenido.seek(0, 2)
        peso = valores.contenido.tell()
        valores.contenido.seek(0)
        valores.peso = peso
        if peso > cls.peso_maximo():
            valores.mensaje_error = 'El-archivo-supera-el-peso-maximo-aceptado'
            valores.codigo = _Constantes.ESTADO._413_NO_CARGADO
            valores.resultado = _Constantes.SALIDA.ALERTA
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


# --------------------------------------------------
# Funcion: crear_modelo
# --------------------------------------------------
def crear_modelo(nombre:str, campos:dict[str, Any]) -> BaseModel:
    return create_model(nombre, **campos)

