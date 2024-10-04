# --------------------------------------------------
# backend\documentos\web_fastapi.py
# --------------------------------------------------

# Importaciones de FastAPI
from fastapi import (
    APIRouter,
    Request,
    Depends,
    Body,
)
from fastapi.responses import (
    JSONResponse,
)

# Importaciones de PySinergIA
from pysinergia import (
    Constantes as C,
)
from pysinergia.web import (
    configurar_microservicio,
)
from pysinergia.web.flask import (
    ComunicadorWeb,
    AutenticadorWeb,
)

# Importaciones del Microservicio
from .dominio import (
    PeticionBuscarDocumentos,
    PeticionVerDocumento,
    PeticionAgregarDocumento,
)
from .adaptadores import (
    ConfigDocumentos,
    ControladorDocumentos,
)

# --------------------------------------------------
# Configuración del Microservicio
aplicacion = 'sinergia'
configuracion = configurar_microservicio(ConfigDocumentos, __file__, aplicacion, None)
autenticador = AutenticadorWeb(configuracion, url_login=f'{configuracion.URL_MICROSERVICIO}/login')
comunicador = ComunicadorWeb(configuracion)
enrutador = APIRouter(prefix=f'{configuracion.PREFIJO_MICROSERVICIO}')

# --------------------------------------------------
# Rutas del Microservicio

async def buscar_documentos(request:Request, peticion:PeticionBuscarDocumentos=Depends()):
    sesion = autenticador.recuperar_sesion()
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    return ControladorDocumentos(configuracion, comunicador).buscar_documentos(peticion)

@enrutador.get('/documentos/{id}', status_code=C.ESTADO._200_EXITO, response_class=JSONResponse)
async def ver_documento(request:Request, peticion:PeticionVerDocumento=Depends()):
    sesion = autenticador.recuperar_sesion()
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    return ControladorDocumentos(configuracion, comunicador).ver_documento(peticion)

@enrutador.post('/documentos', status_code=C.ESTADO._201_CREADO,response_class=JSONResponse)
async def agregar_documento(request:Request, peticion:PeticionAgregarDocumento=Body()):
    sesion = autenticador.recuperar_sesion()
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    return ControladorDocumentos(configuracion, comunicador).agregar_documento(peticion)
