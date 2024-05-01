# backend\prueba\participantes\web.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import (
    APIRouter,
    status,
    Depends,
    Body,
)
from fastapi.responses import JSONResponse
from functools import lru_cache

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia import (
    EmisorWeb,
    RespuestaResultado,
    Configuracion,
    Funciones,
    ErrorPersonalizado,
    Constantes,
)

# --------------------------------------------------
# Importaciones del Servicio personalizado
from .adaptadores import ControladorParticipantes
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    ModeloNuevoParticipante,
    ModeloEditarParticipante,
)

@lru_cache
def obtener_config():
    return Configuracion(_env_file=Funciones.obtener_ruta_env(__name__, modo=None))
config = obtener_config()

# --------------------------------------------------
# Configuración del Servicio personalizado
enrutador = APIRouter(prefix=f"/prueba")

"""
Falta validar token de sesión JWT
Falta validar api_key
"""
# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.get('/participantes',
               status_code=status.HTTP_200_OK,
               response_class=JSONResponse,
               response_model=RespuestaResultado)
async def buscar_participantes(peticion:PeticionBuscarParticipantes=Depends()):
    if peticion:
        raise ErrorPersonalizado('Error personalizadó', 'ERROR', 501, [], aplicacion=config.aplicacion, servicio=config.servicio)
    return ControladorParticipantes(config, EmisorWeb()).buscar_participantes(peticion)

@enrutador.get('/participantes/{id}',
               status_code=status.HTTP_200_OK,
               response_class=JSONResponse)
async def ver_participante(peticion:PeticionParticipante=Depends()):
    return ControladorParticipantes(config, EmisorWeb()).ver_participante(peticion)

@enrutador.post('/participantes',
                status_code=status.HTTP_201_CREATED,
                response_class=JSONResponse)
async def agregar_participante(peticion:ModeloNuevoParticipante=Body()):
    return ControladorParticipantes(config, EmisorWeb()).agregar_participante(peticion)

@enrutador.put('/participantes/{id}',
               status_code=status.HTTP_204_NO_CONTENT,
               response_class=JSONResponse)
async def actualizar_participante(peticion:ModeloEditarParticipante=Body()):
    return ControladorParticipantes(config, EmisorWeb()).actualizar_participante(peticion)

@enrutador.delete('/participantes/{id}',
                  status_code=status.HTTP_204_NO_CONTENT,
                  response_class=JSONResponse)
async def eliminar_participante(peticion:PeticionParticipante=Depends()):
    return ControladorParticipantes(config, EmisorWeb()).eliminar_participante(peticion)
