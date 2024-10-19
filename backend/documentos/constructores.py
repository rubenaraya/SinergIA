# --------------------------------------------------
# backend\documentos\constructores.py
# --------------------------------------------------

import secrets
from typing import Optional

# Importaciones de Pydantic
from pydantic import (Field)

# Importaciones de PySinergIA
from pysinergia.modelos import (Constructor)

# --------------------------------------------------
# Modelo: DocumentoBase
class DocumentoBase(Constructor):
    dto_fuente:str = 'catalogo'
    uid: Optional[str] = Field(
        default='',
        serialization_alias='uid',
        json_schema_extra={'permisos':'','indice':'unico','largo':16}
    )
    titulo: Optional[str] = Field(
        default=None,
        serialization_alias='titulo',
        json_schema_extra={'permisos':'','indice':'simple','largo':250}
    )
    autores: Optional[str] = Field(
        default=None,
        serialization_alias='autores',
        json_schema_extra={'permisos':'','indice':'simple','largo':100}
    )
    editor: Optional[str] = Field(
        default=None,
        serialization_alias='editor',
        json_schema_extra={'permisos':'','indice':'simple','largo':100}
    )
    fechapub: Optional[str] = Field(
        default=None,
        serialization_alias='fechapub',
        json_schema_extra={'permisos':'','indice':'simple','largo':30}
    )
    etiquetas: Optional[str] = Field(
        default=None,
        serialization_alias='etiquetas',
        json_schema_extra={'permisos':'','indice':'simple','largo':250}
    )
    palabras: Optional[str] = Field(
        default=None,
        serialization_alias='palabras',
        json_schema_extra={'permisos':'','indice':'simple','largo':250}
    )
    temasrel: Optional[str] = Field(
        default=None,
        serialization_alias='temasrel',
        json_schema_extra={'permisos':'','indice':'simple','largo':250}
    )
    tipodoc: Optional[str] = Field(
        default=None,
        serialization_alias='tipodoc',
        json_schema_extra={'permisos':'','indice':'simple','largo':30}
    )
    nivcomplejidad: Optional[str] = Field(
        default=None,
        serialization_alias='nivcomplejidad',
        json_schema_extra={'permisos':'','indice':'simple','largo':10}
    )
    coleccion: Optional[str] = Field(
        default=None,
        serialization_alias='coleccion',
        json_schema_extra={'permisos':'','indice':'simple','largo':30}
    )
    estado: Optional[str] = Field(
        default='Activo',
        serialization_alias='estado',
        json_schema_extra={'permisos':'','indice':'simple','largo':10}
    )
    peso: Optional[int] = Field(
        default=0,
        serialization_alias='peso',
        json_schema_extra={'permisos':'','indice':'','largo':11}
    )

# --------------------------------------------------
# Modelo: DocumentoExtra
class DocumentoExtra(Constructor):
    fuente: Optional[str] = Field(
        default=None,
        serialization_alias='fuente',
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
    resumen: Optional[str] = Field(
        default=None,
        serialization_alias='resumen',
        json_schema_extra={'permisos':''}
    )

# --------------------------------------------------
# Modelo: ConstructorListarDocumentos
class ConstructorListarDocumentos(DocumentoBase):
    ...

# --------------------------------------------------
# Modelo: ConstructorAbrirDocumento
class ConstructorAbrirDocumento(DocumentoBase, DocumentoExtra):
    ...

# --------------------------------------------------
# Modelo: ConstructorAgregarDocumento (TODO: Pendiente)
class ConstructorAgregarDocumento(DocumentoBase):
    uid:str = Field(
        default=secrets.token_hex(8),
        serialization_alias='uid',
        json_schema_extra={'formato':'text', 'permisos':''}
    )

# --------------------------------------------------
# Modelo: ConstructorActualizarDocumento (TODO: Pendiente)
class ConstructorActualizarDocumento(DocumentoBase, DocumentoExtra):
    ...

__all__ = ['DocumentoBase', 'ConstructorListarDocumentos', 'ConstructorAbrirDocumento', 'ConstructorAgregarDocumento', 'ConstructorActualizarDocumento']
