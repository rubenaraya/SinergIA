# --------------------------------------------------
# backend\documentos\validadores.py
# --------------------------------------------------

from typing import Optional

# Importaciones de Pydantic
from pydantic import (Field, model_validator)

# Importaciones de PySinergIA
from pysinergia.globales import *
from pysinergia.modelos import (Validador, ValidadorUID)

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

__all__ = ['ValidadorUID', 'ValidadorBuscarDocumentos', 'ValidadorAgregarDocumento', 'ValidadorActualizarDocumento']
