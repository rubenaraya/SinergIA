# backend\prueba\base\enrutador.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from backend.pysinergia.interfaz import Enrutador, ReceptorPeticion, EmisorRespuesta

enrutador = APIRouter()

@enrutador.get('/prueba/base/{accion}', response_class=JSONResponse)
def accion(request:Request, accion: str):
    ruta_plantillas = '/prueba/base/'
    plantillas = Jinja2Templates(directory = f"./backend")
    respuesta = plantillas.TemplateResponse(f".{ruta_plantillas}plantilla_basica.json", context={"request":request})
    return respuesta
