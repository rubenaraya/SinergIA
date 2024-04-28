# backend\prueba\participantes\dominio.py

from typing import Optional, List
from enum import Enum
from uuid import UUID, uuid4
from pydantic import Field

from backend.pysinergia import (Entidad, ModeloPeticion, ModeloRespuesta)

class EntidadParticipante(Entidad):
    def __init__(mi):
        ...

class EstadoParticipante():
    Activo = "Activo"
    Inactivo = "Inactivo"

class Rol(str, Enum):
    Admin = "Admin"
    Usuario = "Usuario"
    Invitado = "Invitado"

class PeticionBuscarParticipantes(ModeloPeticion):
    alias: str | None = Field('')
    email: str | None = Field('')
    estado: str | None = Field('')

class ModeloNuevoParticipante(ModeloPeticion):
    id: Optional[UUID] = uuid4()
    alias: str
    email: str
    rol: Rol

class ModeloEditarParticipante(ModeloPeticion):
    alias: str
    email: str
    rol: Rol
