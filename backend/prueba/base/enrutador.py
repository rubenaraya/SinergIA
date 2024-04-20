# backend\prueba\base\enrutador.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates

prueba_base = APIRouter()

@prueba_base.get('/{aplicacion}/{servicio}')
async def prueba(aplicacion: str, servicio: str):
    return {aplicacion: servicio}

@prueba_base.get('/prueba/base/{accion}', response_class=JSONResponse)
async def accion(request:Request, accion: str):
    ruta_plantillas = '/prueba/base/'
    plantillas = Jinja2Templates(directory = f"./backend")
    respuesta = plantillas.TemplateResponse(f".{ruta_plantillas}plantilla_basica.json", context={"request":request})
    return respuesta
