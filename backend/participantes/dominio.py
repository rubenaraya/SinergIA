# backend\participantes\dominio.py

from enum import Enum
from pydantic import Field
from typing import Optional
from pysinergia._dependencias import (
    Peticion,
    Procedimiento,
)

# --------------------------------------------------
# Clase: EstadoParticipante
# --------------------------------------------------
class EstadoParticipante(str, Enum):
    Activo = 'Activo'
    Inactivo = 'Inactivo'

# --------------------------------------------------
# Clase: RolParticipante
# --------------------------------------------------
class RolParticipante(str, Enum):
    Admin = 'Admin'
    Usuario = 'Usuario'
    Invitado = 'Invitado'

# --------------------------------------------------
# ClaseModelo: PeticionBuscarParticipantes
# --------------------------------------------------
class PeticionBuscarParticipantes(Peticion):
    id: Optional[int] | None = Field(
        default=None,
        serialization_alias='id',
        validation_alias='id',
        json_schema_extra={'orden':'DESC', 'entidad':''}
    )
    alias: Optional[str] | None = Field(
        default=None,
        title='Alias',
        description='Nombre del participante',
        max_length=25,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'filtro':'CONTIENE', 'orden':'', 'entidad':''}
    )
    email: Optional[str] | None = Field(
        default=None,
        title='E-Mail',
        description='Correo-e del participante',
        max_length=50,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'filtro':'CONTIENE', 'orden':'', 'entidad':''}
    )
    estado: Optional[EstadoParticipante] | None = Field(
        default=None,
        title='Estado',
        description='Estado del participante',
        max_length=10,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'filtro':'COINCIDE', 'orden':'', 'entidad':''}
    )
    maximo: Optional[int] | None = Field(serialization_alias='maximo', default=0)
    pagina: Optional[int] | None = Field(serialization_alias='pagina', default=0)

# --------------------------------------------------
# ClaseModelo: ProcedimientoBuscarParticipantes
# --------------------------------------------------
class ProcedimientoBuscarParticipantes(Procedimiento):
    dto_origen_datos: Optional[str] = Field('participantes')
    id: Optional[int] | None = Field(
        default=None,
        title='ID',
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'entidad':''}
    )
    alias: Optional[str] | None = Field(
        default=None,
        title='Alias',
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'entidad':''}
    )
    email: Optional[str] | None = Field(
        default=None,
        title='E-Mail',
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'entidad':''}
    )
    estado: Optional[str] | None = Field(
        default=None,
        title='Estado',
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'entidad':''}
    )

# --------------------------------------------------
# ClaseModelo: PeticionParticipante
# --------------------------------------------------
class PeticionParticipante(Peticion):
    id: Optional[int] | None = Field(
        default=None,
        title='ID',
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )

# --------------------------------------------------
# ClaseModelo: PeticionActualizarParticipante
# --------------------------------------------------
class PeticionActualizarParticipante(PeticionParticipante):
    id: Optional[int] | None = Field(
        default=None,
        title='ID',
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )
    alias: Optional[str] | None = Field(
        default=None,
        title='Alias',
        max_length=25,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )
    email: Optional[str] | None = Field(
        default=None,
        title='E-Mail',
        max_length=50,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )
    estado: Optional[EstadoParticipante] | None = Field(
        default=None,
        title='Estado',
        max_length=10,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )

# --------------------------------------------------
# ClaseModelo: PeticionAgregarParticipante
# --------------------------------------------------
class PeticionAgregarParticipante(Peticion):
    alias: Optional[str] | None = Field(
        default=None,
        title='Alias',
        max_length=25,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )
    email: Optional[str] | None = Field(
        default=None,
        title='E-Mail',
        max_length=50,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )
    estado: Optional[EstadoParticipante] | None = Field(
        default=None,
        title='Estado',
        max_length=10,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'filtro':'', 'orden':'', 'entidad':''}
    )

# --------------------------------------------------
# ClaseModelo: ProcedimientoActualizarParticipante
# --------------------------------------------------
class ProcedimientoActualizarParticipante(Procedimiento):
    dto_origen_datos: Optional[str] = Field('participantes')
    id: Optional[int] | None = Field(
        default=None,
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'formato':'integer', 'permisos':''}
    )
    alias: Optional[str] | None = Field(
        default=None,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    email: Optional[str] | None = Field(
        default=None,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    estado: Optional[str] | None = Field(
        default=None,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'formato':'text', 'permisos':''}
    )

# --------------------------------------------------
# ClaseModelo: ProcedimientoAgregarParticipante
# --------------------------------------------------
class ProcedimientoAgregarParticipante(Procedimiento):
    dto_origen_datos: Optional[str] = Field('participantes')
    alias: Optional[str] | None = Field(
        default=None,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    email: Optional[str] | None = Field(
        default=None,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'formato':'text', 'permisos':''}
    )
    estado: Optional[str] | None = Field(
        default=None,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'formato':'text', 'permisos':''}
    )

# --------------------------------------------------
# ClaseModelo: ProcedimientoEliminarParticipante
# --------------------------------------------------
class ProcedimientoEliminarParticipante(Procedimiento):
    dto_origen_datos: Optional[str] = Field('participantes')
    id: Optional[int] | None = Field(
        default=None,
        validation_alias='id',
        serialization_alias='id',
        json_schema_extra={'formato':'integer', 'permisos':''}
    )

