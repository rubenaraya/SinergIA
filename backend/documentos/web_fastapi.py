# --------------------------------------------------
# backend\documentos\web_fastapi.py
# --------------------------------------------------

# Importaciones de FastAPI
from fastapi import (
    APIRouter,
    Request,
    Depends,
    Body,
    Path,
    Query,
)
from fastapi.responses import (JSONResponse)

# Importaciones de PySinergIA
from pysinergia.config import *
from pysinergia.interfaces.fastapi import *

# Importaciones del Microservicio
from .interacciones import ControladorDocumentos
from .validadores import *

# --------------------------------------------------
# Configuración del Microservicio
app_pwa = 'sinergia'
microservicio = 'documentos'
configuracion = configurar_microservicio(Configuracion, __file__, app_pwa, None)
autenticador = AutenticadorWeb(configuracion, url_login=f'{configuracion.URL_MICROSERVICIO}/login')
comunicador = ComunicadorWeb(configuracion)
enrutador = APIRouter(prefix=f'{configuracion.PREFIJO_MICROSERVICIO}')

# --------------------------------------------------
# Rutas del Microservicio

@enrutador.get(f'/{microservicio}') #dependencies=[Depends(autenticador.validar_token), Depends(autenticador.validar_apikey)]
async def buscar_documentos(request:Request, peticion:ValidadorBuscarDocumentos=Depends()):
    await comunicador.procesar_solicitud(request)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).buscar_documentos(peticion)
    return JSONResponse(respuesta, status_code=codigo)

@enrutador.post(f'/{microservicio}')
async def agregar_documento(request:Request, peticion:ValidadorAgregarDocumento=Body()):
    await comunicador.procesar_solicitud(request)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).agregar_documento(peticion)
    return JSONResponse(respuesta, status_code=codigo)

@enrutador.get(f'/{microservicio}' + '/{uid}')
async def ver_documento(request:Request, uid:str=Path(...)):
    await comunicador.procesar_solicitud(request)
    peticion = ValidadorUID(uid=uid)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).ver_documento(peticion)
    return JSONResponse(respuesta, status_code=codigo)

@enrutador.put(f'/{microservicio}' + '/{uid}')
async def actualizar_documento(request:Request, uid:str=Path(...), peticion:ValidadorActualizarDocumento=Body()):
    await comunicador.procesar_solicitud(request)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).actualizar_documento(peticion)
    return JSONResponse(respuesta, status_code=codigo)

@enrutador.delete(f'/{microservicio}' + '/{uid}')
async def eliminar_documento(request:Request, uid:str=Path(...)):
    await comunicador.procesar_solicitud(request)
    peticion = ValidadorUID(uid=uid)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).eliminar_documento(peticion)
    return JSONResponse(respuesta, status_code=codigo)

