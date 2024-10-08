# --------------------------------------------------
# backend\documentos\modelos.py
# --------------------------------------------------

import secrets
from typing import Optional
from pydantic import Field

# Importaciones de PySinergIA
from pysinergia.modelos import (
    Peticion,
    Procedimiento,
    Respuesta,
)

# --------------------------------------------------
# Modelo: PeticionBuscarDocumentos
class PeticionBuscarDocumentos(Peticion):
    titulo: Optional[str] = Field(
        default=None,
        title='Título',
        description='Título del Documento',
        max_length=200,
        validation_alias='titulo',
        serialization_alias='titulo',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    autores: Optional[str] = Field(
        default=None,
        title='Autores',
        description='Autores del Documento',
        max_length=100,
        validation_alias='autores',
        serialization_alias='autores',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    editor: Optional[str] = Field(
        default=None,
        title='Editor',
        description='Editor del Documento',
        max_length=100,
        validation_alias='editor',
        serialization_alias='editor',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    etiquetas: Optional[str] = Field(
        default=None,
        title='Etiquetas',
        description='Etiquetas del Documento',
        max_length=100,
        validation_alias='etiquetas',
        serialization_alias='etiquetas',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    palabras: Optional[str] = Field(
        default=None,
        title='Palabras',
        description='Palabras Clave del Documento',
        max_length=100,
        validation_alias='palabras',
        serialization_alias='palabras',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    tipodoc: Optional[str] = Field(
        default=None,
        title='Tipo',
        description='Tipo de Documento',
        max_length=50,
        validation_alias='tipodoc',
        serialization_alias='tipodoc',
        json_schema_extra={'filtro':'COINCIDE'}
    )
    coleccion: Optional[str] = Field(
        default=None,
        title='Colección',
        description='Colección',
        max_length=50,
        validation_alias='coleccion',
        serialization_alias='coleccion',
        json_schema_extra={'filtro':'COINCIDE'}
    )
    id: Optional[int] = Field(
        default=None,
        serialization_alias='id',
        validation_alias='id',
        json_schema_extra={'orden':'DESC'}
    )
    maximo: Optional[int] = Field(serialization_alias='maximo', default=10)
    pagina: Optional[int] = Field(serialization_alias='pagina', default=1)

# --------------------------------------------------
# Modelo: RespuestaBuscarDocumentos
class RespuestaBuscarDocumentos(Respuesta):
    def diccionario(mi) -> dict:
        return mi.model_dump(mode='json', warnings=False, exclude_none=True, exclude_unset=True, 
            exclude=('T','D','cookies','fecha','fecha_actual','hora_actual','sesion','url','web')
        )

# --------------------------------------------------
# Modelo: ProcedimientoConsultarDocumentos
class ProcedimientoConsultarDocumentos(Procedimiento):
    dto_origen_datos: Optional[str] = Field('catalogo')
    uid: Optional[str] = Field(
        default=None,
        title='UID',
        validation_alias='uid',
        serialization_alias='uid',
        json_schema_extra={'permisos':''}
    )
    titulo: Optional[str] = Field(
        default=None,
        title='Título',
        validation_alias='titulo',
        serialization_alias='titulo',
        json_schema_extra={'permisos':''}
    )
    autores: Optional[str] = Field(
        default=None,
        title='Autores',
        validation_alias='autores',
        serialization_alias='autores',
        json_schema_extra={'permisos':''}
    )
    editor: Optional[str] = Field(
        default=None,
        title='Editor',
        validation_alias='editor',
        serialization_alias='editor',
        json_schema_extra={'permisos':''}
    )
    tipodoc: Optional[str] = Field(
        default=None,
        title='Tipo Documento',
        validation_alias='tipodoc',
        serialization_alias='tipodoc',
        json_schema_extra={'permisos':''}
    )
    etiquetas: Optional[str] = Field(
        default=None,
        title='Etiquetas',
        validation_alias='etiquetas',
        serialization_alias='etiquetas',
        json_schema_extra={'permisos':''}
    )


# --------------------------------------------------
# Modelo: PeticionVerDocumento
class PeticionVerDocumento(Peticion):
    uid: Optional[str] = Field(
        default=None,
        title='UID',
        validation_alias='uid',
        serialization_alias='uid',
        json_schema_extra={'filtro':'COINCIDE'}
    )

# --------------------------------------------------
# Modelo: PeticionAgregarDocumento
class PeticionAgregarDocumento(Peticion):
    titulo: Optional[str] = Field(
        default=None,
        title='Título',
        max_length=200,
        validation_alias='titulo',
        serialization_alias='titulo',
        json_schema_extra={}
    )

# --------------------------------------------------
# Modelo: ProcedimientoInsertarDocumento
class ProcedimientoInsertarDocumento(Procedimiento):
    dto_origen_datos: Optional[str] = Field('catalogo')
    uid: Optional[str] = Field(
        default=secrets.token_hex(8),
        title='UID',
        validation_alias='uid',
        serialization_alias='uid',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    titulo: Optional[str] = Field(
        default=None,
        validation_alias='titulo',
        serialization_alias='titulo',
        json_schema_extra={'formato':'text', 'permisos':''}
    )

"""
CREATE TABLE "catalogo" (
	"id"	INTEGER NOT NULL UNIQUE,
    "uid"	TEXT NOT NULL UNIQUE,

    "titulo"	TEXT,
	"autores"	TEXT,
	"editor"	TEXT,
	"fechapub"	TEXT,
	"tipodoc"	TEXT,
	"fuente"	TEXT,
    "etiquetas"	TEXT,
	"nivcomplejidad"	TEXT,

    "descripcion"	TEXT,
	"pubobjetivo"	TEXT,
	"temasrel"	TEXT,
	"resumen"	TEXT,
	"palabras"	TEXT,
	
    "coleccion"	TEXT,
	"estado"	TEXT,
	
    "archivo"	TEXT,
	"tipoarch"	TEXT,
	"peso"	INTEGER,
	
    PRIMARY KEY("id" AUTOINCREMENT)
)
"""