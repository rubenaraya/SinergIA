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
    autorizar_acceso,
    concluir_estado,
)

# --------------------------------------------------
# Modelo: Validador
class Validador(BaseModel):
    dto_contexto: Optional[dict] = {}
    dto_roles: Optional[str] = ''

    def adjuntar_contexto(mi, contexto:dict={}):
        mi.dto_contexto = contexto

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
# Modelo: Constructor
class Constructor(BaseModel):
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
                                'formato': field.json_schema_extra.get('formato', 'text'),
                                'entidad': field.json_schema_extra.get('entidad', ''),
                            }
                else:
                    serializado[f'_{field_name}'] = modelo.get(field_name)
        return serializado

# --------------------------------------------------
# Modelo: Presentador
class Presentador(BaseModel):
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
    resultado:dict = {}
    metadatos:dict = {}
    fecha:dict = {}
    web:dict = {}
    url:dict = {}
    sesion:dict = {}
    esquemas:dict = {}
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
                valores.codigo = Constantes.ESTADO._200_EXITO
            else:
                valores.codigo = Constantes.ESTADO._404_NO_ENCONTRADO
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
                    if isinstance(valores.descripcion, str):
                        valores.descripcion = str(_(valores.descripcion)).format(**datos) if valores.descripcion else None
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

    def componer(mi, tipo:str=Constantes.RESPUESTA.BASE) -> dict:
        filtrar = {
            Constantes.RESPUESTA.BASE: ('T','D','cookies','fecha','fecha_actual','hora_actual','sesion','url','web'),
            Constantes.RESPUESTA.API: ('T','D','cookies','fecha','sesion','url','web'),
            Constantes.RESPUESTA.WEB: ('T','D','cookies','web','sesion'),
            Constantes.RESPUESTA.TODO: ('T','D'),
        }
        excluir = filtrar.get(tipo)
        return mi.model_dump(mode='json', warnings=False, exclude_none=True, exclude_unset=True, exclude=excluir)

    def json(mi) -> str:
        return mi.model_dump_json(exclude_none=True, exclude_unset=True, exclude=('T','D'))

