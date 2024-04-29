# backend\prueba\participantes\dominio.py

from typing import Optional, List
from enum import Enum
from pydantic import Field

from backend.pysinergia import (Entidad, ModeloPeticion, ModeloRespuesta)

# --------------------------------------------------
# Clase: EntidadParticipante
# --------------------------------------------------
class EntidadParticipante(Entidad):
    def __init__(mi):
        ...

# --------------------------------------------------
# Clase: EstadoParticipante
# --------------------------------------------------
class EstadoParticipante(str, Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

# --------------------------------------------------
# Clase: Rol
# --------------------------------------------------
class Rol(str, Enum):
    Admin = "Admin"
    Usuario = "Usuario"
    Invitado = "Invitado"

# --------------------------------------------------
# Clase: PeticionBuscarParticipantes
# --------------------------------------------------
class PeticionBuscarParticipantes(ModeloPeticion):
    alias: str | None = Field('', title='Alias', description='Nombre del participante', max_length=25)
    email: str | None = Field('', title='E-Mail', description='Correo-e del participante', max_length=50)
    estado: Optional[EstadoParticipante] | None = Field(None, title='Estado', description='Estado del participante', max_length=10)

# --------------------------------------------------
# Clase: PeticionParticipante
# --------------------------------------------------
class PeticionParticipante(ModeloPeticion):
    id: int = Field(..., title='ID', description='ID del participante', gt=0)

# --------------------------------------------------
# Clase: ModeloNuevoParticipante
# --------------------------------------------------
class ModeloNuevoParticipante(ModeloPeticion):
    alias: str
    email: str
    rol: Rol

# --------------------------------------------------
# Clase: ModeloEditarParticipante
# --------------------------------------------------
class ModeloEditarParticipante(ModeloPeticion):
    id: int
    alias: str
    email: str
    rol: Rol
