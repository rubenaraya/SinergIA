# backend\prueba\participantes\dominio.py

from typing import Optional, List
from enum import Enum
from uuid import UUID, uuid4
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
class EstadoParticipante():
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
    alias: str | None = Field('')
    email: str | None = Field('')
    estado: str | None = Field('')

# --------------------------------------------------
# Clase: PeticionParticipante
# --------------------------------------------------
class PeticionParticipante(ModeloPeticion):
    id: int = Field(None)

# --------------------------------------------------
# Clase: ModeloNuevoParticipante
# --------------------------------------------------
class ModeloNuevoParticipante(ModeloPeticion):
    id: Optional[UUID] = uuid4()
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
