# --------------------------------------------------
# backend\documentos\modelos.py
# --------------------------------------------------

import secrets
from typing import Optional

# Importaciones de Pydantic
from pydantic import (
    Field,
    model_validator,
)

# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes as C,
    ErrorPersonalizado,
)
from pysinergia.modelos import (
    Validador,
    Constructor,
)

"""
PENDIENTES:
- Restaurar el title del Field en cada campo de Validador, para que aparezca en el mensaje de error de validación de Pydantic?.
+ Agregar rutas y todo lo demás para: agregar contenidos a un documento.
"""
# --------------------------------------------------
# MODELOS CONSTRUCTORES

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

# --------------------------------------------------
# MODELOS VALIDADORES

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
                    codigo=C.ESTADO._400_NO_VALIDO,
                    nivel_evento=C.REGISTRO.DEBUG
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

