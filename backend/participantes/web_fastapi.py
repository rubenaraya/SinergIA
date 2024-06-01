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
comunicador = ComunicadorWeb(
    configuracion.web(),
    configuracion.disco(),
    Traductor(configuracion.traductor())
)
autenticador = AutenticadorWeb(
    configuracion.autenticacion(),
    url_login=f'/{configuracion.app_web}/{aplicacion}/login'
)
enrutador = APIRouter(prefix=f'{configuracion.raiz_api}/{aplicacion}')

# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.get('/')
def get_inicio():
    return RedirectResponse(f'/{configuracion.app_web}/{configuracion.frontend}/{aplicacion}/index.html')

@enrutador.get('/participantes',
                status_code=C.ESTADO._200_EXITO,
                #dependencies=[Depends(autenticador.validar_token)]
            )
async def buscar_participantes(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion)
    return Response(content=contenido, headers=encabezados)

@enrutador.get('/participantes/{id}',
                status_code=C.ESTADO._200_EXITO,
                response_class=JSONResponse)
async def ver_participante(request:Request, peticion:PeticionParticipante=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    return Controlador(configuracion, comunicador).ver_participante(peticion)

@enrutador.post('/participantes',
                status_code=C.ESTADO._201_CREADO,
                response_class=JSONResponse)
async def agregar_participante(request:Request, peticion:ModeloNuevoParticipante=Body()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    return Controlador(configuracion, comunicador).agregar_participante(peticion)

@enrutador.put('/participantes/{id}',
                status_code=C.ESTADO._204_VACIO,
                response_class=JSONResponse)
async def actualizar_participante(request:Request, peticion:ModeloEditarParticipante=Body()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    return Controlador(configuracion, comunicador).actualizar_participante(peticion)

@enrutador.delete('/participantes/{id}',
                status_code=C.ESTADO._204_VACIO,
                response_class=JSONResponse)
async def eliminar_participante(request:Request, peticion:PeticionParticipante=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    return Controlador(configuracion, comunicador).eliminar_participante(peticion)


# --------------------------------------------------
# Rutas de pruebas
# --------------------------------------------------

@enrutador.get('/token/{email}',
                status_code=C.ESTADO._200_EXITO,
                response_class=PlainTextResponse)
def token(request:Request, email:str):
    autenticador.firmar_token(email)
    return autenticador.token

@enrutador.get('/login',
                status_code=C.ESTADO._200_EXITO,
                response_class=HTMLResponse)
async def get_login(request:Request):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    return comunicador.transformar_contenido(
        comunicador.transferir_contexto(),
        plantilla='login.html',
        directorio=f'{configuracion.ruta_servicio}/plantillas'
    )

@enrutador.post('/login',
                status_code=C.ESTADO._200_EXITO,
                response_class=JSONResponse)
async def post_login(request:Request):
    respuesta = {}
    return respuesta

@enrutador.get('/pdf', status_code=C.ESTADO._200_EXITO)
async def pdf(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.PDF, guardar=True)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/docx', status_code=C.ESTADO._200_EXITO)
async def docx(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.WORD)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/xlsx', status_code=C.ESTADO._200_EXITO)
async def xlsx(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.EXCEL)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/csv', status_code=C.ESTADO._200_EXITO)
async def csv(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.CSV)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/html', status_code=C.ESTADO._200_EXITO)
async def html(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    contenido, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.FORMATO.HTML)
    return StreamingResponse(content=contenido, headers=encabezados)

# --------------------------------------------------

@enrutador.get('/cargar/{tipo}', status_code=C.ESTADO._200_EXITO, response_class=HTMLResponse)
async def get_cargar(request:Request, tipo:str):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)

    modelos = {"imagen": CargaImagen, "documento": CargaDocumento, "audio": CargaAudio}
    portador_archivo = modelos.get(tipo)
    if not portador_archivo:
        codigo = C.ESTADO._415_NO_SOPORTADO
        salida = ModeloRespuesta(
            codigo=codigo,
            tipo=C.SALIDA.ALERTA,
            mensaje='Tipo-de-carga-no-valido',
            T=comunicador.traspasar_traductor()
        ).diccionario()
        return JSONResponse(salida, status_code=codigo)

    return comunicador.transformar_contenido(
        comunicador.transferir_contexto(),
        plantilla='cargar.html',
        directorio=f'{configuracion.ruta_servicio}/plantillas'
    )

@enrutador.post('/cargar/{tipo}', status_code=C.ESTADO._200_EXITO)
async def post_cargar(request:Request, tipo:str, carga:UploadFile=File(...)):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
 
    modelos = {"imagen": CargaImagen, "documento": CargaDocumento, "audio": CargaAudio}
    portador_archivo = modelos.get(tipo)
    if not portador_archivo:
        codigo = C.ESTADO._415_NO_SOPORTADO
        contenido = ModeloRespuesta(
            codigo=codigo,
            tipo=C.SALIDA.ALERTA,
            mensaje='Tipo-de-carga-no-valido',
            T=comunicador.traspasar_traductor()
        ).diccionario()
    else:
        contenido = Controlador(configuracion, comunicador).cargar_archivo(portador_archivo(origen=carga))
        codigo = contenido.get('codigo', C.ESTADO._200_EXITO)
    return JSONResponse(contenido, status_code=codigo)

