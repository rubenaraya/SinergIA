# --------------------------------------------------
# pysinergia\modelos.py
# --------------------------------------------------

from typing import (
    Optional,
    Self,
)

# Importaciones de Pydantic
from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
)

# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes,
    ValidadorDatos,
    autorizar_acceso,
)

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

