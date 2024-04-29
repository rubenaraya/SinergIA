# backend\prueba\participantes\web.py

from fastapi import APIRouter, status, Depends, Body
from fastapi.responses import JSONResponse

from backend.pysinergia import (
    EmisorWeb,
    RegistradorLogs,
)

from .adaptadores import ControladorParticipantes
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    ModeloNuevoParticipante,
    ModeloEditarParticipante,
)

enrutador = APIRouter(prefix=f"/prueba")
registrador = RegistradorLogs().crear(__name__, RegistradorLogs.NIVEL.DEBUG, './logs/prueba-participantes.log')
registrador.debug("Servicio de Gestión de Participantes")

"""
Falta validar api_key y token de sesión
Falta manejo de excepciones
Falta personalizar respuesta de errores
"""
# --------------------------------------------------
# Rutas personalizadas del servicio
# --------------------------------------------------

@enrutador.get('/participantes',
               status_code=status.HTTP_200_OK,
               response_class=JSONResponse)
async def buscar_participantes(peticion:PeticionBuscarParticipantes=Depends()):
    return ControladorParticipantes(EmisorWeb()).buscar_participantes(peticion)

@enrutador.get('/participantes/{id}',
               status_code=status.HTTP_200_OK,
               response_class=JSONResponse)
async def ver_participante(peticion:PeticionParticipante=Depends()):
    return ControladorParticipantes(EmisorWeb()).ver_participante(peticion)

@enrutador.post('/participantes',
                status_code=status.HTTP_201_CREATED,
                response_class=JSONResponse)
async def agregar_participante(peticion:ModeloNuevoParticipante=Body()):
    return ControladorParticipantes(EmisorWeb()).agregar_participante(peticion)

@enrutador.put('/participantes/{id}',
               status_code=status.HTTP_204_NO_CONTENT,
               response_class=JSONResponse)
async def actualizar_participante(peticion:ModeloEditarParticipante=Body()):
    return ControladorParticipantes(EmisorWeb()).actualizar_participante(peticion)

@enrutador.delete('/participantes/{id}',
                  status_code=status.HTTP_204_NO_CONTENT,
                  response_class=JSONResponse)
async def eliminar_participante(peticion:PeticionParticipante=Depends()):
    return ControladorParticipantes(EmisorWeb()).eliminar_participante(peticion)
