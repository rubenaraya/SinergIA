# --------------------------------------------------
# pysinergia\dominio.py
# --------------------------------------------------

from typing import (
    List,
    Optional,
    Self,
    Any,
)

# Importaciones de Pydantic
from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
)

# Importaciones de PySinergIA
from pysinergia.globales import Constantes

# --------------------------------------------------
# Funcion: autorizar_acceso
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
# Clase: ValidadorDatos
class ValidadorDatos:
    def __init__(mi):
        mi.validaciones = {
            Constantes.VALIDACION.TEXTO: mi._validar_texto,
            Constantes.VALIDACION.ENTERO: mi._validar_entero,
            Constantes.VALIDACION.DECIMAL: mi._validar_decimal,
            Constantes.VALIDACION.FECHA: mi._validar_fecha,
            Constantes.VALIDACION.RUT: mi._validar_rut,
        }
        mi.errores:list = []

    # Métodos privados

    def _validar_texto(mi, minimo:float, maximo:float, valor:Any) -> bool:
        valor = str(valor).strip()
        if maximo > 0 and minimo <= len(valor) <= maximo:
            return True
        elif maximo == 0 and minimo <= len(valor):
            return True
        return False

    def _validar_entero(mi, minimo:float, maximo:float, valor:Any) -> bool:
        valor = int(valor)
        if maximo > 0 and minimo <= valor <= maximo:
            return True
        elif maximo == 0 and minimo <= valor:
            return True
        return False

    def _validar_decimal(mi, minimo:float, maximo:float, valor:Any) -> bool:
        valor = float(valor)
        if maximo > 0 and minimo <= valor <= maximo:
            return True
        elif maximo == 0 and minimo <= valor:
            return True
        return False

    def _validar_fecha(mi, minimo:float, maximo:float, valor:Any) -> bool:
        import datetime
        estado = False
        valor = str(valor)
        if len(valor) > 0 and '-' in valor:
            year, month, day = map(int, valor.split('-'))
            try:
                date = datetime.datetime(year, month, day)
                estado = True
                today = datetime.datetime.today()
                if maximo > 0 and date > today:
                    estado = False
                if minimo > 0 and date < today:
                    estado = False
            except Exception as e:
                print(e)
        elif minimo == 0 and maximo == 0 and len(valor) == 0:
            estado = True
        return estado

    def _validar_rut(mi, minimo:float, maximo:float, valor:Any) -> bool:
        valor = str(valor)
        if (minimo > 0 or len(valor) > 0) and '-' in valor:
            rut, dv = valor.split('-')
            if len(rut) > 0 and len(dv) == 1:
                m, s = 0, 1
                for digit in reversed(rut):
                    s = (s + int(digit) * (9 - m % 6)) % 11
                    m += 1
                calculated_dv = 'k' if s == 10 else str(s)
                if calculated_dv.lower() == dv.lower():
                    return True
        elif minimo == 0 and len(valor) == 0:
            return True
        return False

    def _validar_expreg(mi, patron:str, valor:Any) -> bool:
        import re
        valor = str(valor)
        try:
            if patron and len(valor) > 0:
                while patron.find('\\\\') >0:
                    patron = patron.replace('\\\\', '\\')
                expresion = re.compile('^' + patron + '$')
                if not expresion.match(valor):
                    return False
        except Exception as e:
            print(e)
        return True

    # Métodos públicos

    def verificar_campo(mi, criterios:dict, valor:Any) -> bool:
        if criterios.get('validacion') == 'novalidar':
            return True
        estado = False
        minimo = 0 if not criterios.get('minimo') else float(criterios.get('minimo'))
        maximo = 0 if not criterios.get('maximo') else float(criterios.get('maximo'))
        estado = mi.validaciones.get(criterios.get('validacion'))(minimo, maximo, valor)
        if estado:
            estado = mi._validar_expreg(criterios.get('patron', ''), valor)
        if not estado:
            mensaje = criterios.get('error', '')
            if len(mensaje) >0:
                mi.errores.append({
                    'campo': criterios.get('campo'),
                    'valor': valor,
                    'mensaje': mensaje,
                })
        return estado

# --------------------------------------------------
# Modelo: Diccionario
class Diccionario(BaseModel):
    dto_roles_sesion: Optional[str] = ''
    t: Optional[object] = None

    def _(mi, texto:str) -> str:
        return texto

    def generar(mi) -> dict:
        diccionario = {}
        modelo = mi.model_dump(mode='json', warnings=False, exclude=('t'))
        _ = mi.t if mi.t else mi._
        for campo, datos in modelo.items():
            if not campo.startswith('dto_') and campo not in ['t'] and isinstance(datos, dict):
                diccionario[campo] = {}
                for clave, valores in datos.items():
                    if isinstance(valores, dict):
                        permisos = valores.get('permisos', '')
                        if autorizar_acceso(permisos=permisos, roles=mi.dto_roles_sesion):
                            valor = valores.get('valor', '')
                            diccionario[campo][clave] = {
                                'valor': valor,
                                'etiqueta': _(valores.get('etiqueta', '')),
                                'titulo': _(valores.get('titulo', '')),
                                'estilo': valores.get('estilo', ''),
                                'icono': valores.get('icono', ''),
                                'orden': (valores.get('orden', 1)),
                            }
        return diccionario

# --------------------------------------------------
# Modelo: Peticion
class Peticion(BaseModel):
    dto_contexto: Optional[dict] = {}
    dto_roles_sesion: Optional[str] = ''

    def agregar_contexto(mi, contexto:dict={}):
        mi.dto_contexto = contexto

    def serializar(mi) -> dict:
        serializado = {}
        modelo = mi.model_dump(mode='json', warnings=False, exclude=('T','D'))
        for field_name, field in mi.model_fields.items():
            if field_name not in ['T','D']:
                if not field_name.startswith('dto_'):
                    entrada = field.validation_alias if field.validation_alias else ''
                    salida = field.serialization_alias if field.serialization_alias else entrada
                    valor = modelo.get(field_name)
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
                    serializado[f'_{field_name}'] = modelo.get(field_name)
        return serializado

# --------------------------------------------------
# Modelo: Formulario
class Formulario(Peticion):
    dto_titulo:str = ''
    dto_icono:str = ''
    dto_descripcion:str = ''
    dto_grupos:dict = {}
    dto_acciones:dict = {}
    D: Optional[object] = None
    T: Optional[object] = None

    def _(mi, texto:str) -> str:
        return texto

    def generar(mi) -> dict:
        modelo = mi.model_dump(mode='json', warnings=False, exclude=('T','D','dto_grupos','dto_acciones'))
        _ = mi.T._ if mi.T else mi._
        D = mi.D(dto_roles_sesion=mi.dto_roles_sesion, t=_).generar() if mi.D else None
        formulario:dict = {
            'id': mi.__class__.__name__,
            'icono': mi.dto_icono or '',
            'titulo': _(mi.dto_titulo),
            'descripcion': _(mi.dto_descripcion),
            'ruta': mi.dto_contexto['url']['relativa'] if mi.dto_contexto else '',
            'grupos': {},
            'campos': {},
            'acciones': {},
        }
        for field_name, field in mi.model_fields.items():
            if not field_name.startswith('dto_') and field_name not in ['T','D']:
                entrada = field.validation_alias if field.validation_alias else field_name
                valor = modelo.get(field_name, '') or ''
                if field.json_schema_extra:
                    permisos = field.json_schema_extra.get('permisos', '')
                    if autorizar_acceso(permisos=permisos, roles=mi.dto_roles_sesion):
                        minimo = int(field.json_schema_extra.get('minimo', 0))
                        maximo = int(field.json_schema_extra.get('maximo', 0))
                        error = field.json_schema_extra.get('error', '')
                        if error:
                            error = _(error).replace('(minimo)', str(minimo)).replace('(maximo)', str(maximo))
                        usa_diccionario = field.json_schema_extra.get('diccionario', None)
                        diccionario = D.get(usa_diccionario, {}) if usa_diccionario and D else {}
                        predeterminado = field.default if field.default else None
                        if not valor and predeterminado:
                            valor = predeterminado
                        formulario['campos'][field_name] = {
                            'campo': field_name,
                            'valor': valor,
                            'entrada': entrada,
                            'etiqueta': _(field.title),
                            'descripcion': _(field.description),
                            'grupo': field.json_schema_extra.get('grupo', 'general'),
                            'orden': field.json_schema_extra.get('orden', 1),
                            'vista': field.json_schema_extra.get('vista', 'text'),
                            'alineacion': field.json_schema_extra.get('alineacion', 'end'),
                            'estilo': field.json_schema_extra.get('estilo', ''),
                            'ancho': field.json_schema_extra.get('ancho', 8),
                            'autocompletar': field.json_schema_extra.get('autocompletar', ''),
                            'acepta': field.json_schema_extra.get('acepta', ''),
                            'formato': field.json_schema_extra.get('formato', ''),
                            'editable': field.json_schema_extra.get('editable', True),
                            'requerido': field.json_schema_extra.get('requerido', False),
                            'validacion': field.json_schema_extra.get('validacion', ''),
                            'patron': field.json_schema_extra.get('patron', ''),
                            'minimo': minimo,
                            'maximo': maximo,
                            'error': error,
                            'diccionario': diccionario

                        }
        for clave, valores in mi.dto_grupos.items():
            if isinstance(valores, dict):
                if autorizar_acceso(permisos=valores.get('permisos', ''), roles=mi.dto_roles_sesion):
                    formulario['grupos'][clave] = {
                        'icono': valores.get('icono', ''),
                        'estilo': valores.get('estilo', ''),
                        'visible': valores.get('visible', True),
                        'etiqueta': _(str(valores.get('etiqueta', ''))),
                    }
        for clave, valores in mi.dto_acciones.items():
            if isinstance(valores, dict):
                if autorizar_acceso(permisos=valores.get('permisos', ''), roles=mi.dto_roles_sesion):
                    formulario['acciones'][clave] = {
                        'icono': valores.get('icono', ''),
                        'estilo': valores.get('estilo', ''),
                        'visible': valores.get('visible', True),
                        'funcion': valores.get('funcion', ''),
                        'etiqueta': _(str(valores.get('etiqueta', ''))),
                    }
        return formulario

    def validar(mi, formulario:dict) -> dict:
        validador = ValidadorDatos()

# --------------------------------------------------
# Modelo: Procedimiento
class Procedimiento(BaseModel):
    dto_origen_datos: Optional[str] = ''
    dto_solicitud_datos: Optional[dict] = {}
    dto_roles_sesion: Optional[str] = ''

    def serializar(mi) -> dict:
        serializado:dict = {}
        modelo = mi.model_dump(mode='json', warnings=False, exclude=('T','D'))
        for field_name, field in mi.model_fields.items():
            if field_name not in ['T','D']:
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
                    serializado[f'_{field_name}'] = modelo.get(field_name)
        return serializado

# --------------------------------------------------
# Modelo: Respuesta
class Respuesta(BaseModel):
    model_config = ConfigDict()

    T: Optional[object] = None
    codigo: Optional[int] = None
    conclusion: Optional[str] = None
    mensaje: Optional[str] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_actual:str = ''
    hora_actual:str = ''
    detalles:list = []
    resultado: dict = {}
    metadatos: dict = {}
    fecha: dict = {}
    web: dict = {}
    url: dict = {}
    sesion: dict = {}
    esquemas: dict = {}
    cookies: dict = {}

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
                    if valores.detalles and isinstance(valores.detalles, list):
                        detalles:list = []
                        for error in valores.detalles:
                            if isinstance(error, dict):
                                try:
                                    mensaje:str = _(error.get('_type',''))
                                    ctx = error.get('_ctx', None)
                                    detalles.append({
                                        'clave': error.get('clave'),
                                        'valor': error.get('valor'),
                                        'mensaje': mensaje.format(**ctx) if ctx else mensaje,
                                        '_type': error.get('_type'),
                                        '_msg': error.get('_msg'),
                                        '_ctx': str(ctx) if ctx else ''
                                    })
                                except Exception:
                                    continue
                        valores.detalles = detalles
                except Exception as e:
                    print(e)
        return valores

    def diccionario(mi) -> dict:
        return mi.model_dump(mode='json', warnings=False, exclude_none=True, exclude_unset=True, exclude=('T','D'))

    def json(mi) -> str:
        return mi.model_dump_json(exclude_none=True, exclude_unset=True, exclude=('T','D'))

# --------------------------------------------------
# Modelo: Archivo
class Archivo(BaseModel):
    nombre: Optional[str] = ''
    ruta: Optional[str] = ''
    ubicacion: Optional[str] = ''
    base: Optional[str] = ''
    extension: Optional[str] = ''
    peso: Optional[int] = 0

# --------------------------------------------------
# Modelo: Recurso
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

