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
from pysinergia.globales import (
    Constantes as C,
)
from pysinergia.config import (
    Configuracion,
    configurar_microservicio,
)
from pysinergia.interfaces.fastapi import (
    ComunicadorWeb,
    AutenticadorWeb,
)

# Importaciones del Microservicio
from .modelos import (
    PeticionBuscarDocumentos,
    PeticionVerDocumento,
    PeticionAgregarDocumento,
)
from .operaciones import (
    ControladorDocumentos,
)

# --------------------------------------------------
# Configuración del Microservicio
app_pwa = 'sinergia'
configuracion = configurar_microservicio(Configuracion, __file__, app_pwa, None)
autenticador = AutenticadorWeb(configuracion, url_login=f'{configuracion.URL_MICROSERVICIO}/login')
comunicador = ComunicadorWeb(configuracion)
enrutador = APIRouter(prefix=f'{configuracion.PREFIJO_MICROSERVICIO}')

# --------------------------------------------------
# Rutas del Microservicio

@enrutador.get('/documentos', status_code=C.ESTADO._200_EXITO, response_class=JSONResponse) #dependencies=[Depends(autenticador.validar_token)]
async def buscar_documentos(request:Request, peticion:PeticionBuscarDocumentos=Depends()):
    await comunicador.procesar_solicitud(request)
    return ControladorDocumentos(configuracion, comunicador).buscar_documentos(peticion)

@enrutador.get('/documentos/{id}', status_code=C.ESTADO._200_EXITO, response_class=JSONResponse)
async def ver_documento(request:Request, peticion:PeticionVerDocumento=Depends()):
    await comunicador.procesar_solicitud(request)
    return ControladorDocumentos(configuracion, comunicador).ver_documento(peticion)

@enrutador.post('/documentos', status_code=C.ESTADO._201_CREADO,response_class=JSONResponse)
async def agregar_documento(request:Request, peticion:PeticionAgregarDocumento=Body()):
    await comunicador.procesar_solicitud(request)
    return ControladorDocumentos(configuracion, comunicador).agregar_documento(peticion)

