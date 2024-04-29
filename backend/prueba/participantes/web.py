# backend\prueba\participantes\web.py

from fastapi import APIRouter, status, Depends, Body, HTTPException
from fastapi.responses import JSONResponse

from backend.pysinergia import EmisorWeb, RegistradorLogs

from .adaptadores import ControladorParticipantes as Controlador
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    ModeloNuevoParticipante,
    ModeloEditarParticipante,
)

enrutador = APIRouter(prefix=f"/prueba")
registrador = RegistradorLogs().crear(__name__, RegistradorLogs.NIVEL.DEBUG, './logs/prueba-participantes.log')

"""
Falta validar api_key y token de sesión
Falta manejo de excepciones
Falta personalizar respuesta de errores
"""
@enrutador.get('/participantes', status_code=status.HTTP_200_OK, response_class=JSONResponse)
async def buscar_participantes(peticion:PeticionBuscarParticipantes=Depends()):
    registrador.debug("buscar participantes filtrados")
    return Controlador(EmisorWeb()).buscar_participantes(peticion)

@enrutador.get('/participantes/{id}', status_code=status.HTTP_200_OK, response_class=JSONResponse)
async def ver_participante(peticion:PeticionParticipante=Depends()):
    return Controlador(EmisorWeb()).ver_participante(peticion)

@enrutador.post('/participantes', status_code=status.HTTP_201_CREATED, response_class=JSONResponse)
async def agregar_participante(peticion:ModeloNuevoParticipante=Body()):
    return Controlador(EmisorWeb()).agregar_participante(peticion)

@enrutador.put('/participantes/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=JSONResponse)
async def actualizar_participante(peticion:ModeloEditarParticipante=Body()):
    return Controlador(EmisorWeb()).actualizar_participante(peticion)

@enrutador.delete('/participantes/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=JSONResponse)
async def eliminar_participante(peticion:PeticionParticipante=Depends()):
    return Controlador(EmisorWeb()).eliminar_participante(peticion)
