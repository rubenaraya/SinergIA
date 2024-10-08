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
        max_length=200,
        validation_alias='titulo',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    autores: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias='autores',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    editor: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias='editor',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    etiquetas: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias='etiquetas',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    palabras: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias='palabras',
        json_schema_extra={'filtro':'CONTIENE'}
    )
    tipodoc: Optional[str] = Field(
        default=None,
        max_length=20,
        validation_alias='tipodoc',
        json_schema_extra={'filtro':'COINCIDE'}
    )
    coleccion: Optional[str] = Field(
        default=None,
        max_length=20,
        validation_alias='coleccion',
        json_schema_extra={'filtro':'COINCIDE'}
    )
    id: int = Field(json_schema_extra={'orden':'ASC'}, default=0)
    maximo: int = Field(validation_alias='maximo', default=10)
    pagina: int = Field(validation_alias='pagina', default=1)

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
        serialization_alias='uid',
        json_schema_extra={'permisos':''}
    )
    titulo: Optional[str] = Field(
        default=None,
        serialization_alias='titulo',
        json_schema_extra={'permisos':''}
    )
    autores: Optional[str] = Field(
        default=None,
        serialization_alias='autores',
        json_schema_extra={'permisos':''}
    )
    editor: Optional[str] = Field(
        default=None,
        serialization_alias='editor',
        json_schema_extra={'permisos':''}
    )
    tipodoc: Optional[str] = Field(
        default=None,
        serialization_alias='tipodoc',
        json_schema_extra={'permisos':''}
    )
    etiquetas: Optional[str] = Field(
        default=None,
        serialization_alias='etiquetas',
        json_schema_extra={'permisos':''}
    )


# --------------------------------------------------
# Modelo: PeticionVerDocumento
#TODO: Pendiente
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
#TODO: Pendiente
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
#TODO: Pendiente
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