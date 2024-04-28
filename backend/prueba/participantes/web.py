# backend\prueba\participantes\web.py

from fastapi import APIRouter, status, Depends, Body, HTTPException
from fastapi.responses import JSONResponse

from backend.pysinergia import EmisorWeb

from .adaptadores import ControladorParticipantes as Controlador
from .dominio import (
    PeticionBuscarParticipantes,
    ModeloNuevoParticipante,
    ModeloEditarParticipante
)

instancia = "prueba"
enrutador = APIRouter(prefix=f"/{instancia}")

"""
Falta validar api_key y token de sesión
Falta manejo de excepciones y logger
Falta personalizar respuesta de errores
"""
@enrutador.get('/participantes', response_class=JSONResponse)
async def buscar_participantes(peticion:PeticionBuscarParticipantes=Depends()):
    return Controlador(EmisorWeb()).buscar_participantes(peticion)

@enrutador.get('/participantes/{uid}', response_class=JSONResponse)
async def ver_participante(uid:int):
    peticion = dict({"uid": str(uid)})
    return Controlador(EmisorWeb()).ver_participante(peticion)

@enrutador.post('/participantes', status_code=status.HTTP_201_CREATED, response_class=JSONResponse)
async def agregar_participante(caso:ModeloNuevoParticipante=Body()):
    return Controlador(EmisorWeb()).agregar_participante(caso.model_dump())

@enrutador.put('/participantes/{uid}', response_class=JSONResponse)
async def actualizar_participante(uid:int, caso:ModeloEditarParticipante=Body()):
    return Controlador(EmisorWeb()).actualizar_participante(caso.model_dump())

@enrutador.delete('/participantes/{uid}', status_code=status.HTTP_204_NO_CONTENT, response_class=JSONResponse)
async def eliminar_participante(uid:int):
    peticion = dict({"uid": str(uid)})
    return Controlador(EmisorWeb()).eliminar_participante(peticion)
