# backend\participantes\web_fastapi.py

from pysinergia._dependencias.web_fastapi import *

# --------------------------------------------------
# Importaciones del Servicio personalizado
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    ModeloNuevoParticipante,
    ModeloEditarParticipante,
)
from .adaptadores import (
    ControladorParticipantes as Controlador,
    ConfigParticipantes as ConfigServicio,
)

# --------------------------------------------------
# Configuración del Servicio personalizado
aplicacion = 'prueba'
configuracion = cargar_configuracion(ConfigServicio, __name__, aplicacion, None)
comunicador = ComunicadorWeb(configuracion.contexto(), configuracion.disco())
autenticador = AutenticadorWeb(
    configuracion.autenticacion(),
    url_login=f'/{configuracion.app_web}/{aplicacion}/login'
)
enrutador = APIRouter(prefix=f'{configuracion.raiz_api}/{aplicacion}')

# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.get('')
def get_inicio():
    return RedirectResponse(f'/{configuracion.app_web}/{configuracion.frontend}/{aplicacion}/index.html')

@enrutador.get('/participantes',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=JSONResponse,
                #dependencies=[Depends(autenticador.validar_token)]
            )
def buscar_participantes(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.JSON)
    return Response(content=contenido, headers=encabezados)

@enrutador.get('/participantes/{id}',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=JSONResponse)
def ver_participante(request:Request, peticion:PeticionParticipante=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    return Controlador(configuracion, comunicador).ver_participante(peticion)

@enrutador.post('/participantes',
                status_code=C.ESTADO.HTTP_201_CREADO,
                response_class=JSONResponse)
def agregar_participante(request:Request, peticion:ModeloNuevoParticipante=Body()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    return Controlador(configuracion, comunicador).agregar_participante(peticion)

@enrutador.put('/participantes/{id}',
                status_code=C.ESTADO.HTTP_204_VACIO,
                response_class=JSONResponse)
def actualizar_participante(request:Request, peticion:ModeloEditarParticipante=Body()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    return Controlador(configuracion, comunicador).actualizar_participante(peticion)

@enrutador.delete('/participantes/{id}',
                status_code=C.ESTADO.HTTP_204_VACIO,
                response_class=JSONResponse)
def eliminar_participante(request:Request, peticion:PeticionParticipante=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    return Controlador(configuracion, comunicador).eliminar_participante(peticion)


# --------------------------------------------------
# Rutas de pruebas
# --------------------------------------------------

@enrutador.get('/token/{email}',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=PlainTextResponse)
def token(request:Request, email:str):
    autenticador.firmar_token(email)
    return autenticador.token

@enrutador.get('/login',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=HTMLResponse)
def get_login(request:Request):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    return comunicador.transformar_contenido(
        comunicador.traspasar_contexto(),
        plantilla='login.html',
        directorio=f'{configuracion.ruta_servicio}/plantillas'
    )

@enrutador.post('/login',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=JSONResponse)
def post_login(request:Request):
    respuesta = {}
    return respuesta

@enrutador.get('/pdf', status_code=C.ESTADO.HTTP_200_EXITO)
def pdf(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.PDF, guardar=True)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/docx', status_code=C.ESTADO.HTTP_200_EXITO)
def docx(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.WORD)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/xlsx', status_code=C.ESTADO.HTTP_200_EXITO)
def xlsx(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.EXCEL)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/csv', status_code=C.ESTADO.HTTP_200_EXITO)
def csv(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.CSV)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/html', status_code=C.ESTADO.HTTP_200_EXITO)
def html(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.HTML)
    return StreamingResponse(content=contenido, headers=encabezados)

# --------------------------------------------------

@enrutador.get('/cargar', status_code=C.ESTADO.HTTP_200_EXITO, response_class=HTMLResponse)
def get_cargar(request:Request):
    comunicador.procesar_peticion(request, 'es')
    return comunicador.transformar_contenido(
        comunicador.traspasar_contexto(),
        plantilla='cargar.html',
        directorio=f'{configuracion.ruta_servicio}/plantillas'
    )

"""
Pendiente probar carga con datos (form y json)
"""
@enrutador.post('/cargar', status_code=C.ESTADO.HTTP_200_EXITO)
def post_cargar(request:Request, carga:UploadFile=File(...)):
    try:
        #comunicador.procesar_peticion(request, 'es')
        if not carga:
            return {'mensaje': 'No-se-recibio-carga'}
        if carga.filename == '':
            return {'mensaje': 'La-carga-no-contiene-archivos'}
        tipos_permitidos = [C.MIME.DOCX, C.MIME.XLSX, C.MIME.PPTX, C.MIME.PDF]
        if carga.content_type not in tipos_permitidos:
            return {'mensaje': 'Tipo-de-archivo-no-permitido'}

        """Validar peso máximo ¿usando carga.size?"""
        """Validar que el archivo no exista"""

        #nombre = comunicador.disco.generar_nombre(carga.filename)
        nombre = carga.filename
        destino = f'./tmp/prueba/archivos/{nombre}'
        with open(destino, mode='wb') as archivo:
            while contenido := carga.file.read(1024 * 1024):
                archivo.write(contenido)

    except Exception:
        return {'mensaje': 'Se-produjo-un-error-al-cargar-el-archivo'}
    finally:
        carga.file.close()
    return {'mensaje': f'Archivo-cargado-con-exito: {nombre}'}

"""
    FILE_SIZE = 2097152  # 2MB

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.seek(0)
    if file_size > FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    real_file_size = 0
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too large")
    file.seek(0)
"""
