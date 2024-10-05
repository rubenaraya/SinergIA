# --------------------------------------------------
# pysinergia\archivos.py
# --------------------------------------------------

from typing import (
    List,
    Optional,
    Self,
)

# Importaciones de Pydantic
from pydantic import (
    BaseModel,
    model_validator,
)

# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes,
)

# --------------------------------------------------
# Modelo: Archivo
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class Archivo(BaseModel):
    nombre: Optional[str] = ''
    ruta: Optional[str] = ''
    ubicacion: Optional[str] = ''
    base: Optional[str] = ''
    extension: Optional[str] = ''
    peso: Optional[int] = 0

# --------------------------------------------------
# Modelo: Recurso
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class Recurso(BaseModel):
    conversion: Optional[str] = ''
    tipo_mime: Optional[str] = ''
    extension: Optional[str] = ''

    @model_validator(mode='after')
    @classmethod
    def validate_model(cls, valores:Self) -> 'Recurso':
        if valores.conversion:
            conversiones = {
                Constantes.CONVERSION.PDF: cls._pdf,
                Constantes.CONVERSION.WORD: cls._word,
                Constantes.CONVERSION.EXCEL: cls._excel,
                Constantes.CONVERSION.CSV: cls._csv,
                Constantes.CONVERSION.HTML: cls._html,
                Constantes.CONVERSION.JSON: cls._json,
                Constantes.CONVERSION.TEXTO: cls._texto,
            }
            conversiones.get(valores.conversion)(valores)
        elif valores.tipo_mime:
            tipos = {
                Constantes.MIME.PDF: cls._pdf,
                Constantes.MIME.DOCX: cls._word,
                Constantes.MIME.XLSX: cls._excel,
                Constantes.MIME.CSV: cls._csv,
                Constantes.MIME.HTML: cls._html,
                Constantes.MIME.JSON: cls._json,
                Constantes.MIME.TXT: cls._texto,
            }
            tipos.get(valores.tipo_mime)(valores)
        elif valores.extension:
            extensiones = {
                'pdf': cls._pdf,
                'docx': cls._word,
                'xlsx': cls._excel,
                'csv': cls._csv,
                'html': cls._html,
                'json': cls._json,
                'txt': cls._texto,
            }
            extensiones.get(valores.extension)(valores)
        return valores

    @classmethod
    def _pdf(cls, valores:Self):
        valores.extension = 'pdf'
        valores.conversion = Constantes.CONVERSION.PDF
        valores.tipo_mime = Constantes.MIME.PDF
    @classmethod
    def _word(cls, valores:Self):
        valores.extension = 'docx'
        valores.conversion = Constantes.CONVERSION.WORD
        valores.tipo_mime = Constantes.MIME.DOCX
    @classmethod
    def _excel(cls, valores:Self):
        valores.extension = 'xlsx'
        valores.conversion = Constantes.CONVERSION.EXCEL
        valores.tipo_mime = Constantes.MIME.XLSX
    @classmethod
    def _csv(cls, valores:Self):
        valores.extension = 'csv'
        valores.conversion = Constantes.CONVERSION.CSV
        valores.tipo_mime = Constantes.MIME.CSV
    @classmethod
    def _html(cls, valores:Self):
        valores.extension = 'html'
        valores.conversion = Constantes.CONVERSION.HTML
        valores.tipo_mime = Constantes.MIME.HTML
    @classmethod
    def _json(cls, valores:Self):
        valores.extension = 'json'
        valores.conversion = Constantes.CONVERSION.JSON
        valores.tipo_mime = Constantes.MIME.JSON
    @classmethod
    def _texto(cls, valores:Self):
        valores.extension = 'txt'
        valores.conversion = Constantes.CONVERSION.TEXTO
        valores.tipo_mime = Constantes.MIME.TXT

# --------------------------------------------------
# Modelo: ArchivoCargado
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class ArchivoCargado(BaseModel):
    origen: object
    contenido: object = None
    nombre: Optional[str] = ''
    extension: Optional[str] = ''
    ruta: Optional[str] = ''
    carpeta: Optional[str] = ''
    tipo_mime: Optional[str] = ''
    peso: Optional[int] = 0
    codigo: Optional[int] = Constantes.ESTADO._200_EXITO
    conclusion: Optional[str] = Constantes.CONCLUSION.EXITO
    es_valido: Optional[bool] = False
    mensaje_error: Optional[str] = ''

    RECHAZAR: str = 'RECHAZAR'
    SOBREESCRIBIR: str = 'SOBREESCRIBIR'
    RENOMBRAR: str = 'RENOMBRAR'

    @classmethod
    def tipos_permitidos(cls) -> List[str]:
        ...
    @classmethod
    def peso_maximo(cls) -> int:
        ...

    @model_validator(mode='after')
    @classmethod
    def validate_model(cls, valores:Self) -> 'ArchivoCargado':
        origen = valores.origen
        if not origen:
            valores.mensaje_error = 'No-se-recibio-ninguna-carga'
            valores.codigo = Constantes.ESTADO._422_NO_PROCESABLE
            valores.conclusion = Constantes.CONCLUSION.ALERTA
            return valores
        if origen.filename == '':
            valores.mensaje_error = 'La-carga-recibida-no-contiene-archivo'
            valores.codigo = Constantes.ESTADO._400_NO_VALIDO
            valores.conclusion = Constantes.CONCLUSION.ALERTA
            return valores
        valores.nombre = origen.filename
        valores.extension = valores.nombre.rsplit('.', 1)[1].lower()
        if origen.content_type not in cls.tipos_permitidos():
            valores.mensaje_error = 'El-tipo-de-archivo-no-esta-permitido'
            valores.codigo = Constantes.ESTADO._415_NO_SOPORTADO
            valores.conclusion = Constantes.CONCLUSION.ALERTA
            return valores
        valores.tipo_mime = origen.content_type
        valores.contenido = origen.file if hasattr(origen, 'file') else origen.stream
        valores.contenido.seek(0, 2)
        peso = valores.contenido.tell()
        valores.contenido.seek(0)
        valores.peso = peso
        if peso > cls.peso_maximo():
            valores.mensaje_error = 'El-archivo-supera-el-peso-maximo-aceptado'
            valores.codigo = Constantes.ESTADO._413_NO_CARGADO
            valores.conclusion = Constantes.CONCLUSION.ALERTA
            return valores
        valores.es_valido = True
        return valores

# --------------------------------------------------
# Modelo: ImagenCargada
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class ImagenCargada(ArchivoCargado):
    carpeta: Optional[str] = 'imagenes'

    @classmethod
    def tipos_permitidos(cls) -> List[str]:
        return [
            Constantes.MIME.JPG,
            Constantes.MIME.JPEG,
            Constantes.MIME.PNG,
        ]
    @classmethod
    def peso_maximo(cls) -> int:
        return 5 * Constantes.PESO.MB

# --------------------------------------------------
# Modelo: DocumentoCargado
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class DocumentoCargado(ArchivoCargado):
    carpeta: Optional[str] = 'documentos'

    @classmethod
    def tipos_permitidos(cls) -> List[str]:
        return [
            Constantes.MIME.DOCX,
            Constantes.MIME.DOC,
            Constantes.MIME.XLSX,
            Constantes.MIME.XLS,
            Constantes.MIME.PPTX,
            Constantes.MIME.PPT,
            Constantes.MIME.PDF,
            Constantes.MIME.CSV,
        ]
    @classmethod
    def peso_maximo(cls) -> int:
        return 2 * Constantes.PESO.MB

# --------------------------------------------------
# Modelo: AudioCargado
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class AudioCargado(ArchivoCargado):
    carpeta: Optional[str] = 'audios'

    @classmethod
    def tipos_permitidos(cls) -> List[str]:
        return [
            Constantes.MIME.MP3,
            Constantes.MIME.WAV,
            Constantes.MIME.OGG,
            Constantes.MIME.OPUS,
            Constantes.MIME.WMA,
            Constantes.MIME.WEBA,
        ]
    @classmethod
    def peso_maximo(cls) -> int:
        return 25 * Constantes.PESO.MB

# --------------------------------------------------
# Modelo: VideoCargado
"""
PROPOSITO:
RESPONSABILIDADES:
"""
class VideoCargado(ArchivoCargado):
    carpeta: Optional[str] = 'videos'
    @classmethod
    def tipos_permitidos(cls) -> List[str]:
        return [
            Constantes.MIME.MP4,
            Constantes.MIME.WEBM,
            Constantes.MIME.WMV,
        ]
    @classmethod
    def peso_maximo(cls) -> int:
        return 25 * Constantes.PESO.MB
