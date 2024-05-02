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
from pysinergia.globales import (
    Funciones,
    Constantes,
    ErrorPersonalizado,
)
from pysinergia.servicio import RespuestaResultado
from pysinergia.web import (
    ComunicadorWeb,
)

# --------------------------------------------------
# Importaciones del Servicio personalizado
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    ModeloNuevoParticipante,
    ModeloEditarParticipante,
)
from .adaptadores import (
    ControladorParticipantes as Controlador,
    ConfigParticipantes as Config,
)
from . import api_keys

@lru_cache
def obtener_config(entorno:str=None):
    return Config(_env_file=Funciones.obtener_ruta_env(__name__, entorno=entorno))

# --------------------------------------------------
# Configuración del Servicio personalizado
config = obtener_config(None)
enrutador = APIRouter(prefix=f"/prueba")
comunicador = ComunicadorWeb(api_keys)

"""
Falta validar token de sesión JWT
"""
# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.get('/participantes',
               status_code=status.HTTP_200_OK,
               response_class=JSONResponse,
               response_model=RespuestaResultado,
               # dependencies=[Depends(comunicador.validar_apikey)]
               )
async def buscar_participantes(peticion:PeticionBuscarParticipantes=Depends()):
    return Controlador(config, comunicador).buscar_participantes(peticion)

@enrutador.get('/participantes/{id}',
               status_code=status.HTTP_200_OK,
               response_class=JSONResponse)
async def ver_participante(peticion:PeticionParticipante=Depends()):
    return Controlador(config, comunicador).ver_participante(peticion)

@enrutador.post('/participantes',
                status_code=status.HTTP_201_CREATED,
                response_class=JSONResponse)
async def agregar_participante(peticion:ModeloNuevoParticipante=Body()):
    return Controlador(config, comunicador).agregar_participante(peticion)

@enrutador.put('/participantes/{id}',
               status_code=status.HTTP_204_NO_CONTENT,
               response_class=JSONResponse)
async def actualizar_participante(peticion:ModeloEditarParticipante=Body()):
    return Controlador(config, comunicador).actualizar_participante(peticion)

@enrutador.delete('/participantes/{id}',
                  status_code=status.HTTP_204_NO_CONTENT,
                  response_class=JSONResponse)
async def eliminar_participante(peticion:PeticionParticipante=Depends()):
    return Controlador(config, comunicador).eliminar_participante(peticion)
