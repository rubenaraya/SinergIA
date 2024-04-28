# backend\prueba\participantes\web.py

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from backend.pysinergia import EmisorWeb

from .adaptadores import ControladorParticipantes as Controlador
from .dominio import ModeloNuevoParticipante, ModeloEditarParticipante

instancia = "prueba"
enrutador = APIRouter(prefix=f"/{instancia}")

"""
Falta validar api_key y token de sesión
Falta recuperar petición real y valdar con pydantic (serializar)
"""
@enrutador.get('/participantes', response_class=JSONResponse)
async def buscar_participantes():
    peticion = {"instancia": instancia}
    return Controlador(EmisorWeb()).buscar_participantes(peticion)

@enrutador.post('/participantes', status_code=status.HTTP_201_CREATED, response_class=JSONResponse)
async def agregar_participante(caso:ModeloNuevoParticipante):
    peticion = caso
    return Controlador(EmisorWeb()).agregar_participante(peticion)

@enrutador.get('/participantes/{uid}', response_class=JSONResponse)
async def ver_participante(uid:int):
    peticion = {"instancia": instancia, "uid": uid}
    return Controlador(EmisorWeb()).ver_participante(peticion)

@enrutador.put('/participantes/{uid}', response_class=JSONResponse)
async def actualizar_participante(caso:ModeloEditarParticipante, uid:int):
    peticion = caso
    return Controlador(EmisorWeb()).actualizar_participante(peticion)

@enrutador.delete('/participantes/{uid}', status_code=status.HTTP_204_NO_CONTENT, response_class=JSONResponse)
async def eliminar_participante(uid:int):
    peticion = {"instancia": instancia, "uid": uid}
    return Controlador(EmisorWeb()).eliminar_participante(peticion)
