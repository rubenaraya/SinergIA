# --------------------------------------------------
# pysinergia\modelos.py
# --------------------------------------------------

from abc import ABC
from datetime import (date, datetime)
from typing import (Optional, Self, Union, Any, get_args, get_origin)

# Importaciones de Pydantic
from pydantic import (BaseModel, ConfigDict, Field, model_validator)

# Importaciones de PySinergIA
from pysinergia.globales import (autorizar_acceso, concluir_estado)

# --------------------------------------------------
# Clases de Constantes:
class VISTA:
    CHECKBOX = 'checkbox'
    COLOR = 'color'
    DATE = 'date'
    EMAIL = 'email'
    HIDDEN = 'hidden'
    IMAGE = 'image'
    LABEL = 'label'
    NUMBER = 'number'
    PASSWORD = 'password'
    RADIO = 'radio'
    SEARCH = 'search'
    SELECT = 'select'
    SWITCH = 'switch'
    TEL = 'tel'
    TEXT = 'text'
    TEXTAREA = 'textarea'
    TIME = 'time'
    URL = 'url'

class VALIDACION:
    TEXTO = 'texto'
    ENTERO = 'entero'
    DECIMAL = 'decimal'
    RUT = 'rut'
    OPCIONES = 'opciones'
    FECHA = 'fecha'
    NOVALIDAR = 'novalidar'

class COMPOSICION:
    BASE = 'BASE'
    API = 'API'
    WEB = 'WEB'
    TODO = 'TODO'

# --------------------------------------------------
# Modelo: Validador
class Validador(ABC, BaseModel):
    dto_contexto: Optional[dict] = {}
    dto_roles: Optional[str] = ''

    """
    def adjuntar_contexto(mi, contexto:dict={}):
        mi.dto_contexto = contexto
    """

    def convertir(mi) -> dict:
        serializado = {}
        modelo = mi.model_dump(mode='json', warnings=False, exclude=('T','D'))
        for field_name, field in mi.model_fields.items():
            if field_name not in ['T','D']:
                if not field_name.startswith('dto_'):
                    entrada = field.validation_alias if field.validation_alias else field_name
                    salida = field.serialization_alias if field.serialization_alias else entrada
                    valor = modelo.get(field_name)
                    if field.json_schema_extra:
                        permisos = field.json_schema_extra.get('permisos', '')
                        if autorizar_acceso(permisos=permisos, roles=mi.dto_roles):
                            serializado[field_name] = {
                                'campo': field_name,
                                'entrada': entrada,
                                'salida': salida,
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
# Modelo: ValidadorUID
class ValidadorUID(Validador):
    uid:str = Field(
        validation_alias='uid',
        json_schema_extra={'filtro':'COINCIDE', 'permisos':''}
    )
    @model_validator(mode='before')
    def validar_uid(cls, values):
        uid = values.get('uid')
        if not isinstance(uid, str) or len(uid) != 16 or not all(c in '0123456789abcdefABCDEF' for c in uid):
            raise Exception('El-uid-no-es-valido')
        return values

# --------------------------------------------------
# Modelo: Constructor
class Constructor(ABC, BaseModel):
    dto_solicitud:dict = {}
    dto_roles: Optional[str] = ''
    dto_fuente: Optional[str] = ''

    def organizar(mi) -> dict:
        serializado:dict = {}
        modelo = mi.model_dump(mode='json', warnings=False, exclude=('T','D'))
        for field_name, field in mi.model_fields.items():
            if field_name not in ['T','D']:
                if not field_name.startswith('dto_'):
                    entrada = field.validation_alias if field.validation_alias else ''
                    salida = field.serialization_alias if field.serialization_alias else ''
                    if field.json_schema_extra:
                        permisos = field.json_schema_extra.get('permisos', '')
                        if autorizar_acceso(permisos=permisos, roles=mi.dto_roles):
                            serializado[field_name] = {
                                'campo': field_name,
                                'entrada': entrada or '',
                                'salida': salida or '',
                                'etiqueta': field.title or '',
                                'default': field.default,
                                'formato': field.json_schema_extra.get('formato', 'text'),
                                'entidad': field.json_schema_extra.get('entidad', ''),
                                'indice': field.json_schema_extra.get('indice', ''),
                                'largo': field.json_schema_extra.get('largo', 255),
                            }
                else:
                    serializado[f'_{field_name}'] = modelo.get(field_name)
        return serializado

    def definiciones(mi) -> dict:
        serializado:dict = {}
        tipos_aceptados = {str, int, float, bool, date, datetime}
        for field_name, field in mi.model_fields.items():
            if field_name not in ['T','D']:
                if not field_name.startswith('dto_') and field.json_schema_extra:
                    field_type = mi.__annotations__.get(field_name)
                    if get_origin(field_type) is Union:
                        field_type = next(t for t in get_args(field_type) if t is not type(None))
                    serializado[field_name] = {
                        'default': field.default,
                        'tipo': field_type.__name__ if field_type in tipos_aceptados else '',
                        'indice': field.json_schema_extra.get('indice', ''),
                        'largo': field.json_schema_extra.get('largo', 0),
                    }
        return serializado

# --------------------------------------------------
# Modelo: Presentador
class Presentador(ABC, BaseModel):
    model_config = ConfigDict()

    T: Optional[object] = None
    codigo: Optional[int] = None
    conclusion: Optional[str] = None
    mensaje: Optional[str] = None
    titulo: Optional[str] = None
    fecha_actual:str = ''
    hora_actual:str = ''
    detalles:list = []
    resultado:dict = {}
    metadatos:dict = {}
    fecha:dict = {}
    web:dict = {}
    url:dict = {}
    sesion:dict = {}
    cookies:dict = {}

    @model_validator(mode='after')
    @classmethod
    def model_validator(cls, valores:Self) -> 'Presentador':
        from collections import ChainMap

        def _filtrar_diccionario(diccionario:dict):
            if diccionario and isinstance(diccionario, dict):
                return {k: v for k, v in diccionario.items() if isinstance(v, (str, int, float, bool))}
            return {}

        if not valores.codigo:
            if valores.resultado:
                total = valores.resultado.get('total', 0)
                if total == -1:
                    valores.codigo = 500
                elif total == 0:
                    valores.codigo = 404
                else:
                    valores.codigo = 200
            else:
                valores.codigo = 404
        if not valores.conclusion:
            valores.conclusion = concluir_estado(valores.codigo)
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
                    if valores.detalles and isinstance(valores.detalles, list):
                        detalles:list = []
                        for error in valores.detalles:
                            if isinstance(error, dict):
                                try:
                                    mensaje:str = _(error.get('_msg',''))
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

    def componer(mi, tipo:str=COMPOSICION.BASE) -> dict:
        filtrar = {
            COMPOSICION.BASE: ('T','D','cookies','fecha','fecha_actual','hora_actual','sesion','url','web'),
            COMPOSICION.API: ('T','D','cookies','fecha','sesion','url','web'),
            COMPOSICION.WEB: ('T','D','cookies','web','sesion'),
            COMPOSICION.TODO: ('T','D'),
        }
        excluir = filtrar.get(tipo)
        return mi.model_dump(mode='json', warnings=False, exclude_none=True, exclude_unset=True, exclude=excluir)

    def json(mi) -> str:
        return mi.model_dump_json(exclude_none=True, exclude_unset=True, exclude=('T','D'))

# --------------------------------------------------
# Modelo: Diccionario
class Diccionario(ABC, BaseModel):
    dto_roles: Optional[str] = ''
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
                        if autorizar_acceso(permisos=permisos, roles=mi.dto_roles):
                            valor = valores.get('valor', '')
                            diccionario[campo][clave] = {
                                'valor': valor,
                                'etiqueta': _(valores.get('etiqueta', '')),
                                'estilo': valores.get('estilo', ''),
                                'titulo': _(valores.get('titulo', '')),
                                'icono': valores.get('icono', ''),
                                'orden': (valores.get('orden', 1)),
                            }
        return diccionario

# --------------------------------------------------
# Modelo: Formulario
class Formulario(Validador):
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
        D:dict = mi.D(dto_roles=mi.dto_roles, t=_).generar() if mi.D else None
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
                    if autorizar_acceso(permisos=permisos, roles=mi.dto_roles):
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
                if autorizar_acceso(permisos=valores.get('permisos', ''), roles=mi.dto_roles):
                    formulario['grupos'][clave] = {
                        'icono': valores.get('icono', ''),
                        'estilo': valores.get('estilo', ''),
                        'visible': valores.get('visible', True),
                        'etiqueta': _(str(valores.get('etiqueta', ''))),
                    }
        for clave, valores in mi.dto_acciones.items():
            if isinstance(valores, dict):
                if autorizar_acceso(permisos=valores.get('permisos', ''), roles=mi.dto_roles):
                    formulario['acciones'][clave] = {
                        'icono': valores.get('icono', ''),
                        'estilo': valores.get('estilo', ''),
                        'visible': valores.get('visible', True),
                        'funcion': valores.get('funcion', ''),
                        'etiqueta': _(str(valores.get('etiqueta', ''))),
                    }
        return formulario

    def verificar(mi, formulario:dict) -> dict:
        estado = True
        definicion:dict
        verificador = VerificadorCampos()
        for definicion in formulario:
            valor = definicion.get('valor', '')
            if isinstance(valor, list):
                valor = ','.join(valor)
            valor = valor.strip()
            if len(verificador.verificar(definicion=definicion, valor=valor)) > 0:
                estado = False
        return estado

# --------------------------------------------------
# Clase: VerificadorCampos
class VerificadorCampos(ABC):
    def __init__(mi):
        mi.validaciones = {
            VALIDACION.TEXTO: mi._validar_texto,
            VALIDACION.ENTERO: mi._validar_entero,
            VALIDACION.DECIMAL: mi._validar_decimal,
            VALIDACION.FECHA: mi._validar_fecha,
            VALIDACION.RUT: mi._validar_rut,
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
        estado = False
        valor = str(valor)
        if len(valor) > 0 and '-' in valor:
            year, month, day = map(int, valor.split('-'))
            try:
                date = datetime(year, month, day)
                estado = True
                today = datetime.today()
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

    def verificar(mi, definicion:dict, valor:Any) -> str:
        validacion = definicion.get('validacion')
        mensaje = ''
        if validacion == 'novalidar':
            return mensaje
        estado = False
        minimo = 0 if not definicion.get('minimo') else float(definicion.get('minimo'))
        maximo = 0 if not definicion.get('maximo') else float(definicion.get('maximo'))
        estado = mi.validaciones.get(validacion)(minimo, maximo, valor)
        if estado:
            estado = mi._validar_expreg(definicion.get('patron', ''), valor)
        if not estado:
            campo = definicion.get('campo')
            etiqueta = str(definicion.get('etiqueta', campo))
            mensaje = str(definicion.get('error', 'ERROR'))
            if len(mensaje) >0:
                mensaje = mensaje.replace('(minimo)', str(minimo))
                mensaje = mensaje.replace('(maximo)', str(maximo))
                mensaje = mensaje.replace('(etiqueta)', etiqueta)
                mensaje = mensaje.replace('(campo)', campo)
                mi.errores.append({
                    'campo': campo,
                    'valor': valor,
                    'mensaje': mensaje,
                })
        return mensaje

