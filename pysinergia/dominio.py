# pysinergia\dominio.py

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Dominio)
from typing import (
    Dict,
    List,
    Optional,
    Self,
    #Tuple,
    #Literal,
    #Any,
)
#from enum import Enum
from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
    #field_validator,
    #Field,
)

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia import Constantes

# --------------------------------------------------
# Funcion: autorizar_acceso
# --------------------------------------------------
def autorizar_acceso(roles:str, permisos:str=None) -> bool:
    if permisos == '':
        return True
    if permisos and roles:
        if permisos == '*':
            return True
        eval_permisos = set(permisos.split(','))
        eval_roles = set(roles.split(','))
        if bool(eval_permisos & eval_roles):
            return True
    return False

# --------------------------------------------------
# ClaseModelo: Peticion
# --------------------------------------------------
class Peticion(BaseModel):
    dto_contexto: Optional[dict] | None = {}
    dto_roles_sesion: Optional[str] | None = ''

    def agregar_contexto(mi, contexto:dict={}):
        mi.dto_contexto = contexto

    def serializar(mi) -> dict:
        serializado = {}
        datos = mi.model_dump(mode='json', warnings=False)
        for field_name, field in mi.model_fields.items():
            if not field_name.startswith('dto_'):
                entrada = field.validation_alias if field.validation_alias else ''
                salida = field.serialization_alias if field.serialization_alias else ''
                valor = datos.get(field_name)
                if field.json_schema_extra:
                    permisos = field.json_schema_extra.get('permisos', '')
                    if autorizar_acceso(permisos=permisos, roles=mi.dto_roles_sesion):
                        serializado[field_name] = {
                            'campo': field_name,
                            'entrada': entrada or '',
                            'salida': salida or '',
                            'etiqueta': field.title or '',
                            'filtro': field.json_schema_extra.get('filtro', ''),
                            'orden': field.json_schema_extra.get('orden', ''),
                            'entidad': field.json_schema_extra.get('entidad', ''),
                            'valor': valor or ''
                        }
                else:
                    serializado[field_name] = valor
            else:
                serializado[f'_{field_name}'] = datos.get(field_name)
        return serializado

# --------------------------------------------------
# ClaseModelo: Procedimiento
# --------------------------------------------------
class Procedimiento(BaseModel):
    dto_origen_datos: Optional[str] | None = ''
    dto_solicitud_datos: Optional[dict] | None = {}
    dto_roles_sesion: Optional[str] | None = ''

    def serializar(mi) -> dict:
        serializado:dict = {}
        datos = mi.model_dump(mode='json', warnings=False)
        for field_name, field in mi.model_fields.items():
            if not field_name.startswith('dto_'):
                entrada = field.validation_alias if field.validation_alias else ''
                salida = field.serialization_alias if field.serialization_alias else ''
                if field.json_schema_extra:
                    permisos = field.json_schema_extra.get('permisos', '')
                    if autorizar_acceso(permisos=permisos, roles=mi.dto_roles_sesion):
                        serializado[field_name] = {
                            'campo': field_name,
                            'entrada': entrada or '',
                            'salida': salida or '',
                            'etiqueta': field.title or '',
                            'formato': field.json_schema_extra.get('formato', 'text'),
                            'entidad': field.json_schema_extra.get('entidad', ''),
                        }
            else:
                serializado[f'_{field_name}'] = datos.get(field_name)
        return serializado

# --------------------------------------------------
# ClaseModelo: Respuesta
# --------------------------------------------------
class Respuesta(BaseModel):
    model_config = ConfigDict()

    T: object | None = None
    codigo: Optional[int] | None = None
    conclusion: Optional[str] | None = None
    mensaje: Optional[str] | None = None
    titulo: Optional[str] | None = None
    descripcion: Optional[str] | None = None
    fecha_actual:str = ''
    hora_actual:str = ''
    detalles:list = []
    resultado: dict | None = {}
    metadatos: dict | None = {}
    fecha: dict | None = {}
    web: dict | None = {}
    url: dict | None = {}
    sesion: dict | None = {}
    esquemas: dict | None = {}
    cookies: dict | None = {}

    @model_validator(mode='after')
    @classmethod
    def model_validator(cls, valores:Self) -> 'Respuesta':
        from collections import ChainMap

        def _filtrar_diccionario(diccionario:dict):
            if diccionario and isinstance(diccionario, dict):
                return {k: v for k, v in diccionario.items() if isinstance(v, (str, int, float, bool))}
            return {}
        
        if not valores.codigo:
            valores.codigo = Constantes.ESTADO._200_EXITO
        if not valores.conclusion:
            valores.conclusion = Constantes.CONCLUSION.EXITO
        if valores.T:
            fechahora = valores.T.fecha_hora()
            valores.fecha_actual = fechahora.get('fecha')
            valores.hora_actual = fechahora.get('hora')
            _ = valores.T.abrir_traduccion()
            if _:
                datos = ChainMap(_filtrar_diccionario(valores.resultado), _filtrar_diccionario(valores.metadatos), fechahora)
                try:
                    valores.mensaje = str(_(valores.mensaje)).format(**datos) if valores.mensaje else None
                    valores.titulo = str(_(valores.titulo)).format(**datos) if valores.titulo else None
                    if isinstance(valores.descripcion, str):
                        valores.descripcion = str(_(valores.descripcion)).format(**datos) if valores.descripcion else None
                except Exception as e:
                    print(e)
        return valores

    def diccionario(mi) -> Dict:
        return mi.model_dump(mode='json', exclude_none=True, exclude_unset=True, exclude=('T'))

    def json(mi) -> str:
        return mi.model_dump_json(exclude_none=True, exclude_unset=True, exclude=('T'))

# --------------------------------------------------
# ClaseModelo: ArchivoCargado
# --------------------------------------------------
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
# ClaseModelo: ImagenCargada
# --------------------------------------------------
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
        return 5 * 1024 * 1024

# --------------------------------------------------
# ClaseModelo: DocumentoCargado
# --------------------------------------------------
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
        return 2 * 1024 * 1024

# --------------------------------------------------
# ClaseModelo: AudioCargado
# --------------------------------------------------
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
        return 25 * 1024 * 1024

# --------------------------------------------------
# ClaseModelo: VideoCargado
# --------------------------------------------------
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
# ClaseModelo: Recurso
# --------------------------------------------------
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
# ClaseModelo: Formulario
# --------------------------------------------------
class Formulario(Peticion):
    dto_titulo:str = ''
    dto_icono:str = ''
    dto_intro:str = ''
    dto_grupos:dict = {}
    dto_interacciones:dict = {}
    T: object | None = None

    def _(mi, texto:str) -> str:
        return texto

    def generar(mi) -> dict:
        datos = mi.model_dump(mode='json', warnings=False, exclude=('T','dto_grupos','dto_interacciones'))
        _ = mi.T._ if mi.T else mi._
        formulario:dict = {
            'id': mi.__class__,
            'icono': mi.dto_icono or '',
            'leyendas': {'titulo': _(mi.dto_titulo), 'intro': _(mi.dto_intro)},
            'campos': {},
            'grupos': {},
            'interacciones': {},
        }
        for field_name, field in mi.model_fields.items():
            if not field_name.startswith('dto_') and field_name not in ['T']:
                entrada = field.validation_alias if field.validation_alias else ''
                valor = datos.get(field_name)
                if field.json_schema_extra:
                    permisos = field.json_schema_extra.get('permisos', '')
                    if autorizar_acceso(permisos=permisos, roles=mi.dto_roles_sesion):
                        minimo = str(field.json_schema_extra.get('minimo', 0))
                        maximo = str(field.json_schema_extra.get('maximo', 0))
                        msg_error = field.json_schema_extra.get('msg_error', '')
                        if msg_error:
                            msg_error = _(msg_error)
                            msg_error = msg_error.replace('(minimo)', minimo)
                            msg_error = msg_error.replace('(maximo)', maximo)
                        diccionario = field.json_schema_extra.get('diccionario', None)
                        if diccionario:
                            # serializar diccionario
                            ...

                        formulario['campos'][field_name] = {
                            'campo': field_name,
                            'entrada': entrada or '',
                            'etiqueta': field.title or '',
                            'descripcion': field.description or '',
                            'grupo': field.json_schema_extra.get('grupo', ''),
                            'vista': field.json_schema_extra.get('vista', ''),
                            'autocompletar': field.json_schema_extra.get('autocompletar', ''),
                            'tipo_val': field.json_schema_extra.get('tipo_val', ''),
                            'requerido': '1' if field.json_schema_extra.get('requerido', False) else '0',
                            'editable': '1' if field.json_schema_extra.get('editable', True) else '0',
                            'minimo': minimo,
                            'maximo': maximo,
                            'msg_error': msg_error or '',
                            'valor': valor or '',
                            'diccionario': {}
                        }
                else:
                    formulario['campos'][field_name] = valor
        # procesar dto_grupos y dto_interacciones
        
        return formulario

# --------------------------------------------------
# ClaseModelo: Diccionario
# --------------------------------------------------
class Diccionario(BaseModel):
    dto_roles_sesion: Optional[str] | None = ''

    def serializar(mi) -> dict:
        serializado:dict = {}

        return serializado

# --------------------------------------------------
# ClaseModelo: Informe
# --------------------------------------------------
class Informe(BaseModel):
    dto_roles_sesion: Optional[str] | None = ''
    dto_titulo:str = ''
    dto_icono:str = ''
    dto_intro:str = ''
    dto_grupos:dict = {}
    dto_interacciones:dict = {}

    def serializar(mi) -> dict:
        serializado:dict = {}

        return serializado

