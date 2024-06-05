# backend\participantes\dominio.py

from pysinergia._dependencias.dominio import *

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
    origen_datos: Optional[str] = Field('participantes')
    alias: Optional[str] = Field(
        default='',
        title='Alias',
        description='Nombre del participante',
        max_length=25,
        validation_alias='nombre',
        serialization_alias='alias',
        json_schema_extra={'formato': 'text', 'filtro': 'CONTIENE', 'orden': '', 'entidad': 'participantes', 'visible': True}
    )
    email: Optional[str] = Field(
        default='',
        title='E-Mail',
        description='Correo-e del participante',
        max_length=50,
        validation_alias='email',
        serialization_alias='email',
        json_schema_extra={'formato': 'email', 'filtro': 'CONTIENE', 'orden': '', 'entidad': '', 'visible': True}
    )
    estado: Optional[EstadoParticipante] | None = Field(
        default='',
        title='Estado',
        description='Estado del participante',
        max_length=10,
        validation_alias='estado',
        serialization_alias='estado',
        json_schema_extra={'formato': 'text', 'filtro': 'COINCIDE', 'orden': '', 'entidad': '', 'visible': False}
    )
    id: Optional[str] | None = Field(
        default='',
        serialization_alias='id',
        validation_alias='id',
        json_schema_extra={'formato': 'integer', 'orden': 'DESC', 'entidad': 'participantes', 'visible': True}
    )

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
