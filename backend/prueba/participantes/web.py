# backend\prueba\participantes\web.py

# --------------------------------------------------
# Importaciones de Infraestructura Web
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
    Body,
)
from fastapi.responses import JSONResponse

# --------------------------------------------------
# Importaciones de PySinergIA
from backend.pysinergia import (
    EmisorWeb,
    RegistradorLogs,
    RespuestaResultado,
    Configuracion,
    Funciones,
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

# --------------------------------------------------
# Configuración del Servicio personalizado
config = Configuracion(_env_file=Funciones.obtener_ruta_env(__name__, modo=None))
enrutador = APIRouter(prefix=f"/prueba")
registrador = RegistradorLogs().crear(__name__, config.nivel_registro, config.archivo_logs)

"""
Falta manejo de excepciones y errores
Falta personalizar formato de respuesta de errores
Falta incluir códigos de estado en RespuestaResultado
Falta traducir códigos internos en códigos de estado HTTP
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
    return ControladorParticipantes(config, EmisorWeb()).buscar_participantes(peticion)

@enrutador.get('/participantes/{id}',
               status_code=status.HTTP_200_OK,
               response_class=JSONResponse)
async def ver_participante(peticion:PeticionParticipante=Depends()):
    try:
        return ControladorParticipantes(config, EmisorWeb()).ver_participante(peticion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 

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
