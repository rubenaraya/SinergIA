# backend\participantes\dominio.py

from pysinergia._dependencias import (Peticion, Procedimiento)
from pydantic import Field
from typing import Optional
from enum import Enum

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
    id: Optional[str] | None = Field(
        default='',
        serialization_alias='id',
        validation_alias='id',
        json_schema_extra={'orden':'DESC', 'entidad':''}
    )
    alias: Optional[str] = Field(
        default='',
        title='Alias',
        description='Nombre del participante',
        max_length=25,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'filtro':'CONTIENE', 'orden':'', 'entidad':''}
    )
    email: Optional[str] = Field(
        default='',
        title='E-Mail',
        description='Correo-e del participante',
        max_length=50,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'filtro':'CONTIENE', 'orden':'', 'entidad':''}
    )
    estado: Optional[EstadoParticipante] | str = Field(
        default='',
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
    origen_datos: Optional[str] = Field('participantes')
    alias: Optional[str] | None = Field(
        default='',
        title='Alias',
        validation_alias='alias',
        serialization_alias='nombre',
        json_schema_extra={'entidad':''}
    )
    email: Optional[str] | None = Field(
        default='',
        title='E-Mail',
        validation_alias='email',
        serialization_alias='',
        json_schema_extra={'entidad':''}
    )
    estado: Optional[str] | None = Field(
        default='',
        title='Estado',
        validation_alias='estado',
        serialization_alias='',
        json_schema_extra={'entidad':''}
    )

# --------------------------------------------------
# ClaseModelo: PeticionParticipante
# --------------------------------------------------
class PeticionParticipante(Peticion):
    id: Optional[int] | None = Field(
        default='',
        #serialization_alias='id',
        validation_alias='id',
        json_schema_extra={'filtro':'COINCIDE'}
    )

# --------------------------------------------------
# ClaseModelo: ProcedimientoActualizarParticipante
# --------------------------------------------------
class ProcedimientoActualizarParticipante(Procedimiento):
    origen_datos: Optional[str] = Field('participantes')
    id: Optional[int] | None = Field(
        default='',
        validation_alias='id',
        json_schema_extra={'formato':'integer'}
    )
    alias: Optional[str] | None = Field(
        default='',
        validation_alias='alias',
        json_schema_extra={'formato':'text'}
    )
    email: Optional[str] | None = Field(
        default='',
        validation_alias='email',
        json_schema_extra={'formato':'text'}
    )
    estado: Optional[str] | None = Field(
        default='',
        validation_alias='estado',
        json_schema_extra={'formato':'text'}
    )

# --------------------------------------------------
# ClaseModelo: ModeloNuevoParticipante
# --------------------------------------------------
class ModeloNuevoParticipante(Peticion):
    ...

# --------------------------------------------------
# ClaseModelo: ModeloEditarParticipante
# --------------------------------------------------
class ModeloEditarParticipante(ModeloNuevoParticipante):
    ...

