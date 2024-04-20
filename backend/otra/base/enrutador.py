# backend\otra\base\enrutador.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates

enrutador = APIRouter()

@enrutador.get('/otra/base/{accion}', response_class=JSONResponse)
def accion(request:Request, accion: str):
    ruta_plantillas = '/otra/base/'
    plantillas = Jinja2Templates(directory = f"./backend")
    respuesta = plantillas.TemplateResponse(f".{ruta_plantillas}plantilla_basica.json", context={"request":request})
    return respuesta
