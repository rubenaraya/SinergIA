from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from backend.pysinergia.infra_web import Emisor
from backend.prueba.controlador import ControladorParticipantes as Controlador

instancia = "prueba"
enrutador = APIRouter(prefix=f"/{instancia}")

"""
Falta validar api_key y token de sesión
Falta recuperar petición real y valdar con pydantic (serializar)
Falta archivo para manejar las configuraciones en infra y servicios
"""
@enrutador.get('/participantes', response_class=JSONResponse)
def buscar_participantes():
    peticion = {"instancia": instancia}
    return Controlador(Emisor()).buscar_participantes(peticion)

@enrutador.post('/participantes', response_class=JSONResponse)
def agregar_participante():
    peticion = {"instancia": instancia}
    return Controlador(Emisor()).agregar_participante(peticion)

@enrutador.get('/participantes/{uid}', response_class=JSONResponse)
def ver_participante(uid:int):
    peticion = {"instancia": instancia, "uid": uid}
    return Controlador(Emisor()).ver_participante(peticion)

@enrutador.put('/participantes/{uid}', response_class=JSONResponse)
def actualizar_participante(uid:int):
    peticion = {"instancia": instancia, "uid": uid}
    return Controlador(Emisor()).actualizar_participante(peticion)

@enrutador.delete('/participantes/{uid}', response_class=JSONResponse)
def eliminar_participante(uid:int):
    peticion = {"instancia": instancia, "uid": uid}
    return Controlador(Emisor()).eliminar_participante(peticion)
