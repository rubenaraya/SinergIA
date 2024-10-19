# --------------------------------------------------
# backend\documentos\validadores.py
# --------------------------------------------------

from typing import Optional

# Importaciones de Pydantic
from pydantic import (Field, model_validator)

# Importaciones de PySinergIA
from pysinergia.globales import *
from pysinergia.modelos import (Validador, Formulario)

# --------------------------------------------------
# Modelo: ValidadorBuscarDocumentos
class ValidadorBuscarDocumentos(Validador):
    titulo: Optional[str] = Field(
        default=None,
        max_length=250,
        validation_alias='titulo',
        json_schema_extra={'filtro':'CONTIENE', 'permisos':''}
    )
    autores: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias='autores',
        json_schema_extra={'filtro':'CONTIENE', 'permisos':''}
    )
    editor: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias='editor',
        json_schema_extra={'filtro':'CONTIENE', 'permisos':''}
    )
    etiquetas: Optional[str] = Field(
        default=None,
        max_length=250,
        validation_alias='etiquetas',
        json_schema_extra={'filtro':'CONTIENE', 'permisos':''}
    )
    palabras: Optional[str] = Field(
        default=None,
        max_length=250,
        validation_alias='palabras',
        json_schema_extra={'filtro':'CONTIENE', 'permisos':''}
    )
    tipodoc: Optional[str] = Field(
        default=None,
        max_length=30,
        validation_alias='tipodoc',
        json_schema_extra={'filtro':'COINCIDE', 'permisos':''}
    )
    coleccion: Optional[str] = Field(
        default=None,
        max_length=30,
        validation_alias='coleccion',
        json_schema_extra={'filtro':'COINCIDE', 'permisos':''}
    )
    id:int = Field(json_schema_extra={'orden':'ASC'}, default=0)
    maximo:int = Field(validation_alias='maximo', default=10)
    pagina:int = Field(validation_alias='pagina', default=1)

# --------------------------------------------------
# Modelo: ValidadorConsultarDocumento
class ValidadorConsultarDocumento(Validador):
    uid:str = Field(
        validation_alias='uid',
        json_schema_extra={'filtro':'COINCIDE', 'permisos':''}
    )
    @model_validator(mode='before')
    def validar_uid(cls, values):
        uid = values.get('uid')
        if not isinstance(uid, str) or len(uid) != 16 or not all(c in '0123456789abcdefABCDEF' for c in uid):
            raise ErrorPersonalizado(
                    mensaje='El-uid-no-es-valido',
                    codigo=Constantes.ESTADO._400_NO_VALIDO,
                    nivel_evento=Constantes.REGISTRO.DEBUG
                )
        return values

# --------------------------------------------------
# Modelo: ValidadorBaseDocumento (TODO: Pendiente)
class ValidadorBaseDocumento(Validador):
    titulo:str = Field(
        max_length=250,
        validation_alias='titulo',
        json_schema_extra={'permisos':''}
    )

# --------------------------------------------------
# Modelo: ValidadorAgregarDocumento (TODO: Pendiente)
class ValidadorAgregarDocumento(ValidadorBaseDocumento):
    ...

# --------------------------------------------------
# Modelo: ValidadorActualizarDocumento (TODO: Pendiente)
class ValidadorActualizarDocumento(ValidadorBaseDocumento):
    ...

# --------------------------------------------------
# Modelo: FormActualizarDocumento (TODO: Pendiente)
class FormActualizarDocumento(Formulario):
    ...

__all__ = ['ValidadorBuscarDocumentos', 'ValidadorConsultarDocumento', 'ValidadorAgregarDocumento', 'ValidadorActualizarDocumento', 'FormActualizarDocumento']
