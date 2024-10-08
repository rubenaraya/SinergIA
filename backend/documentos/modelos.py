# --------------------------------------------------
# backend\documentos\modelos.py
# --------------------------------------------------

import secrets
from typing import Optional
from pydantic import Field, model_validator

# Importaciones de PySinergIA
from pysinergia.modelos import (
    Peticion,
    Operacion,
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
# Modelo: DocumentoMetadatos
class DocumentoMetadatos(Operacion):
    dto_origen_datos: Optional[str] = Field('catalogo')
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
    etiquetas: Optional[str] = Field(
        default=None,
        serialization_alias='etiquetas',
        json_schema_extra={'permisos':''}
    )
    palabras: Optional[str] = Field(
        default=None,
        serialization_alias='palabras',
        json_schema_extra={'permisos':''}
    )
    tipodoc: Optional[str] = Field(
        default=None,
        serialization_alias='tipodoc',
        json_schema_extra={'permisos':''}
    )
    coleccion: Optional[str] = Field(
        default=None,
        serialization_alias='coleccion',
        json_schema_extra={'permisos':''}
    )
    estado: Optional[str] = Field(
        default='Activo',
        serialization_alias='estado',
        json_schema_extra={'formato':'text', 'permisos':''}
    )

# --------------------------------------------------
# Modelo: DocumentoCompleto
class DocumentoCompleto(DocumentoMetadatos):
    fechapub: Optional[str] = Field(
        default=None,
        serialization_alias='fechapub',
        json_schema_extra={'permisos':''}
    )
    fuente: Optional[str] = Field(
        default=None,
        serialization_alias='fuente',
        json_schema_extra={'permisos':''}
    )
    nivcomplejidad: Optional[str] = Field(
        default=None,
        serialization_alias='nivcomplejidad',
        json_schema_extra={'permisos':''}
    )
    descripcion: Optional[str] = Field(
        default=None,
        serialization_alias='descripcion',
        json_schema_extra={'permisos':''}
    )
    pubobjetivo: Optional[str] = Field(
        default=None,
        serialization_alias='pubobjetivo',
        json_schema_extra={'permisos':''}
    )
    temasrel: Optional[str] = Field(
        default=None,
        serialization_alias='temasrel',
        json_schema_extra={'permisos':''}
    )
    resumen: Optional[str] = Field(
        default=None,
        serialization_alias='resumen',
        json_schema_extra={'permisos':''}
    )

# --------------------------------------------------
# Modelo: OperacionConsultarDocumentos
class OperacionConsultarDocumentos(DocumentoMetadatos):
    uid: Optional[str] = Field(
        default=None,
        serialization_alias='uid',
        json_schema_extra={'permisos':''}
    )

# --------------------------------------------------
# Modelo: PeticionVerDocumento
class PeticionVerDocumento(Peticion):
    uid: str = Field(
        validation_alias='uid',
        json_schema_extra={'filtro':'COINCIDE'}
    )
    @model_validator(mode='before')
    def validar_uid(cls, values):
        uid = values.get('uid')
        if not isinstance(uid, str) or len(uid) != 16 or not all(c in '0123456789abcdefABCDEF' for c in uid):
            raise ValueError("El-uid-debe-ser-una-cadena-de-16-caracteres")
        return values

# --------------------------------------------------
# Modelo: OperacionVerDocumento
class OperacionVerDocumento(DocumentoCompleto):
    uid: Optional[str] = Field(
        default=None,
        serialization_alias='uid',
        json_schema_extra={'permisos':''}
    )


# --------------------------------------------------
# Modelo: PeticionAgregarDocumento
#TODO: Pendiente
class PeticionAgregarDocumento(Peticion):
    titulo: str = Field(
        max_length=200,
        validation_alias='titulo',
        json_schema_extra={}
    )

# --------------------------------------------------
# Modelo: OperacionInsertarDocumento
#TODO: Pendiente
class OperacionInsertarDocumento(DocumentoCompleto):
    uid: str = Field(
        default=secrets.token_hex(8),
        serialization_alias='uid',
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