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
    PeticionConsultarDocumento,
    PeticionAgregarDocumento,
    PeticionActualizarDocumento,
)
from .interacciones import (
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

@enrutador.get('/documentos') #dependencies=[Depends(autenticador.validar_token), Depends(autenticador.validar_apikey)]
async def buscar_documentos(request:Request, peticion:PeticionBuscarDocumentos=Depends()):
    await comunicador.procesar_solicitud(request)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).buscar_documentos(peticion)
    return JSONResponse(respuesta, status_code=codigo)

@enrutador.post('/documentos')
async def agregar_documento(request:Request, peticion:PeticionAgregarDocumento=Body()):
    await comunicador.procesar_solicitud(request)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).agregar_documento(peticion)
    return JSONResponse(respuesta, status_code=codigo)

@enrutador.get('/documentos/{uid}')
async def ver_documento(request:Request, uid:str):
    await comunicador.procesar_solicitud(request)
    peticion = PeticionConsultarDocumento(uid=uid)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).ver_documento(peticion)
    return JSONResponse(respuesta, status_code=codigo)

@enrutador.put('/documentos/{uid}')
async def actualizar_documento(request:Request, uid:str, peticion:PeticionActualizarDocumento=Body()):
    await comunicador.procesar_solicitud(request)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).actualizar_documento(peticion)
    return JSONResponse(respuesta, status_code=codigo)

@enrutador.delete('/documentos/{uid}')
async def eliminar_documento(request:Request, uid:str):
    await comunicador.procesar_solicitud(request)
    peticion = PeticionConsultarDocumento(uid=uid)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).eliminar_documento(peticion)
    return JSONResponse(respuesta, status_code=codigo)

