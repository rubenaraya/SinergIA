# backend\prueba\participantes\dominio.py

from typing import Optional, List, Annotated
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

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

class ModeloBuscarParticipantes(ModeloPeticion):
    alias: str | None = ''
    email: str | None = ''
    estado: str | None = ''

class ModeloNuevoParticipante(BaseModel):
    id: Optional[UUID] = uuid4()
    alias: str
    email: str
    rol: Rol

class ModeloEditarParticipante(BaseModel):
    alias: str
    email: str
    rol: Rol
