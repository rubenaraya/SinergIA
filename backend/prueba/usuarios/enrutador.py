# backend\prueba\usuarios\enrutador.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from backend.pysinergia.infraestructura import Enrutador, ReceptorPeticion, EmisorRespuesta

# --------------------------------------------------
# Rutas personalizadas del Servicio Usuarios
# --------------------------------------------------
enrutador = APIRouter()

@enrutador.get('/prueba/usuarios/{accion}', response_class=JSONResponse)
def accion(request:Request, accion: str):
    ruta_plantillas = '/prueba/usuarios/'
    plantillas = Jinja2Templates(directory = f"./backend")
    respuesta = plantillas.TemplateResponse(f".{ruta_plantillas}plantilla.json", context={"request":request})
    return respuesta
