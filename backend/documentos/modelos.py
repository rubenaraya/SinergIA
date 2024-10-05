# --------------------------------------------------
# backend\documentos\modelos.py
# --------------------------------------------------

from typing import Optional
from pydantic import Field

# Importaciones de PySinergIA
from pysinergia.modelos import (
    Peticion,
    Procedimiento,
)

# --------------------------------------------------
# Modelo: PeticionBuscarDocumentos
class PeticionBuscarDocumentos(Peticion):
    id: Optional[int] = Field(
        default=None,
        serialization_alias='id',
        validation_alias='id',
        json_schema_extra={'orden':'DESC', 'entidad':''}
    )
    titulo: Optional[str] = Field(
        default=None,
        title='Título',
        description='Título del Documento',
        max_length=100,
        validation_alias='titulo',
        serialization_alias='titulo',
        json_schema_extra={'filtro':'CONTIENE', 'orden':'', 'entidad':''}
    )
    palabras: Optional[str] = Field(
        default=None,
        title='Palabras',
        description='Palabras clave o etiquetas',
        max_length=250,
        validation_alias='palabras',
        serialization_alias='palabras',
        json_schema_extra={'filtro':'CONTIENE', 'orden':'', 'entidad':''}
    )
    estado: Optional[str] = Field(
        default=None,
        title='Estado',
        description='Estado del Documento',
        max_length=10,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'filtro':'COINCIDE', 'orden':'', 'entidad':''}
    )
    maximo: Optional[int] = Field(serialization_alias='maximo', default=0)
    pagina: Optional[int] = Field(serialization_alias='pagina', default=0)

# --------------------------------------------------
# Modelo: PeticionDocumento
class PeticionVerDocumento(Peticion):
    id: Optional[int] = Field(
        default=None,
        title='ID',
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )

# --------------------------------------------------
# Modelo: PeticionAgregarDocumento
class PeticionAgregarDocumento(Peticion):
    titulo: Optional[str] = Field(
        default=None,
        title='Título',
        max_length=100,
        validation_alias='titulo',
        serialization_alias='titulo',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )
    palabras: Optional[str] = Field(
        default=None,
        title='Palabras',
        max_length=250,
        validation_alias='palabras',
        serialization_alias='palabras',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )
    estado: Optional[str] = Field(
        default=None,
        title='Estado',
        max_length=10,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )

# --------------------------------------------------
# Modelo: ProcedimientoBuscarDocumentos
class ProcedimientoBuscarDocumentos(Procedimiento):
    dto_origen_datos: Optional[str] = Field('catalogo')
    id: Optional[int] = Field(
        default=None,
        title='ID',
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'entidad':''}
    )
    titulo: Optional[str] = Field(
        default=None,
        title='Título',
        validation_alias='titulo',
        serialization_alias='titulo',
        json_schema_extra={'entidad':''}
    )
    palabras: Optional[str] = Field(
        default=None,
        title='Palabras',
        validation_alias='palabras',
        serialization_alias='palabras',
        json_schema_extra={'entidad':''}
    )
    estado: Optional[str] = Field(
        default=None,
        title='Estado',
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'entidad':''}
    )

# --------------------------------------------------
# Modelo: ProcedimientoAgregarDocumento
class ProcedimientoAgregarDocumento(Procedimiento):
    dto_origen_datos: Optional[str] = Field('catalogo')
    titulo: Optional[str] = Field(
        default=None,
        validation_alias='titulo',
        serialization_alias='titulo',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    palabras: Optional[str] = Field(
        default=None,
        validation_alias='palabras',
        serialization_alias='palabras',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    estado: Optional[str] = Field(
        default=None,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'formato':'text', 'permisos':''}
    )

