# backend\prueba\participantes\dominio.py

from typing import (Optional, List, Dict, Tuple)
from enum import Enum

# --------------------------------------------------
# Importaciones de bibliotecas (capa de Dominio)
from pydantic import Field

# --------------------------------------------------
# Importaciones de PySinergIA
from pysinergia.dominio import (
    Entidad,
    ModeloPeticion,
)

# --------------------------------------------------
# Clase: EntidadParticipante
# --------------------------------------------------
class EntidadParticipante(Entidad):
        ...

# --------------------------------------------------
# Clase: EstadoParticipante
# --------------------------------------------------
class EstadoParticipante(str, Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

# --------------------------------------------------
# Clase: RolParticipante
# --------------------------------------------------
class RolParticipante(str, Enum):
    Admin = "Admin"
    Usuario = "Usuario"
    Invitado = "Invitado"

# --------------------------------------------------
# ClaseModelo: PeticionBuscarParticipantes
# --------------------------------------------------
class PeticionBuscarParticipantes(ModeloPeticion):
    alias: str | None = Field('', title='Alias', description='Nombre del participante', max_length=25)
    email: str | None = Field('', title='E-Mail', description='Correo-e del participante', max_length=50)
    estado: Optional[EstadoParticipante] | None = Field(None, title='Estado', description='Estado del participante', max_length=10)

# --------------------------------------------------
# ClaseModelo: PeticionParticipante
# --------------------------------------------------
class PeticionParticipante(ModeloPeticion):
    id: int = Field(..., title='ID', description='ID del participante', gt=0)

# --------------------------------------------------
# ClaseModelo: ModeloNuevoParticipante
# --------------------------------------------------
class ModeloNuevoParticipante(ModeloPeticion):
    alias: str
    email: str
    rol: RolParticipante

# --------------------------------------------------
# ClaseModelo: ModeloEditarParticipante
# --------------------------------------------------
class ModeloEditarParticipante(ModeloNuevoParticipante):
    id: int
