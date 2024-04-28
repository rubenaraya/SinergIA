# backend\prueba\participantes\dominio.py

from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

from backend.pysinergia import Entidad, Rol

class EntidadParticipante(Entidad):
    def __init__(mi):
        ...

class Estado():
    Activo = "Activo"
    Inactivo = "Inactivo"

class ModeloNuevoParticipante(BaseModel):
    id: Optional[UUID] = uuid4()
    alias: str
    rol: Rol

class ModeloEditarParticipante(BaseModel):
    alias: str
    rol: Rol
