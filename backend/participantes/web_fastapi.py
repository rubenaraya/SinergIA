# backend\participantes\web_fastapi.py

from pysinergia._dependencias import (
    configurar_microservicio,
    C,
    Traductor,
    ImagenCargada,
    DocumentoCargado,
    AudioCargado,
    Respuesta,
)
from pysinergia._dependencias.web_fastapi import *

# --------------------------------------------------
# Importaciones del Microservicio personalizado
from .dominio import (
    PeticionBuscarParticipantes,
    PeticionParticipante,
    PeticionActualizarParticipante,
    PeticionAgregarParticipante,
    ProcedimientoAgregarParticipante,
    ProcedimientoActualizarParticipante,
    ProcedimientoEliminarParticipante,
    ProcedimientoBuscarParticipantes,
)
from .adaptadores import (
    ControladorParticipantes as Controlador,
    ConfigParticipantes as ConfigMicroservicio,
)

# --------------------------------------------------
# Configuración del Microservicio personalizado
configuracion = configurar_microservicio(ConfigMicroservicio, __file__, 'prueba', None)

comunicador = ComunicadorWeb(
    configuracion.web(),
    configuracion.disco(),
    Traductor(configuracion.traductor())
)
autenticador = AutenticadorWeb(
    configuracion.autenticacion(),
    url_login=f'{configuracion.URL_MICROSERVICIO}/login'
)
enrutador = APIRouter(prefix=f'{configuracion.PREFIJO_MICROSERVICIO}')

# --------------------------------------------------
# Rutas del Microservicio personalizado
# --------------------------------------------------

@enrutador.get('/')
def get_inicio():
    return RedirectResponse(f'/{configuracion.APP_GLOBAL}/{configuracion.ALIAS_FRONTEND}/{configuracion.APLICACION}/index.html')

@enrutador.get('/participantes',
                status_code=C.ESTADO._200_EXITO,
                #dependencies=[Depends(autenticador.validar_token)]
            )
async def buscar_participantes(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    cuerpo, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, conversion=C.CONVERSION.JSON)
    return Response(content=cuerpo, headers=encabezados)

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
async def agregar_participante(request:Request, peticion:PeticionAgregarParticipante=Body()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    return Controlador(configuracion, comunicador).agregar_participante(peticion)

@enrutador.put('/participantes/{id}',
                status_code=C.ESTADO._204_VACIO,
                response_class=JSONResponse)
async def actualizar_participante(request:Request, peticion:PeticionActualizarParticipante=Body()):
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
    cuerpo, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.CONVERSION.PDF, guardar=True)
    return StreamingResponse(content=cuerpo, headers=encabezados)

@enrutador.get('/docx', status_code=C.ESTADO._200_EXITO)
async def docx(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    cuerpo, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.CONVERSION.WORD)
    return StreamingResponse(content=cuerpo, headers=encabezados)

@enrutador.get('/xlsx', status_code=C.ESTADO._200_EXITO)
async def xlsx(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    cuerpo, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.CONVERSION.EXCEL)
    return StreamingResponse(content=cuerpo, headers=encabezados)

@enrutador.get('/csv', status_code=C.ESTADO._200_EXITO)
async def csv(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    cuerpo, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.CONVERSION.CSV)
    return StreamingResponse(content=cuerpo, headers=encabezados)

@enrutador.get('/html', status_code=C.ESTADO._200_EXITO)
async def html(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
    cuerpo, encabezados = Controlador(configuracion, comunicador).buscar_participantes(peticion, C.CONVERSION.HTML)
    return StreamingResponse(content=cuerpo, headers=encabezados)

# --------------------------------------------------

@enrutador.get('/cargar/{tipo}', status_code=C.ESTADO._200_EXITO, response_class=HTMLResponse)
async def get_cargar(request:Request, tipo:str):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)

    modelos = {"imagen": ImagenCargada, "documento": DocumentoCargado, "audio": AudioCargado}
    portador_archivo = modelos.get(tipo)
    if not portador_archivo:
        codigo = C.ESTADO._415_NO_SOPORTADO
        respuesta = Respuesta(
            codigo=codigo,
            conclusion=C.CONCLUSION.ALERTA,
            mensaje='Tipo-de-carga-no-valido',
            T=comunicador.traspasar_traductor()
        ).diccionario()
        return JSONResponse(respuesta, status_code=codigo)

    return comunicador.transformar_contenido(
        comunicador.transferir_contexto(),
        plantilla='cargar.html',
        ruta_plantillas=f'{configuracion.RUTA_MICROSERVICIO}/plantillas'
    )

@enrutador.post('/cargar/{tipo}', status_code=C.ESTADO._200_EXITO)
async def post_cargar(request:Request, tipo:str, carga:UploadFile=File(...)):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    await comunicador.procesar_peticion(request, idioma, sesion)
 
    modelos = {"imagen": ImagenCargada, "documento": DocumentoCargado, "audio": AudioCargado}
    portador_archivo = modelos.get(tipo)
    if not portador_archivo:
        codigo = C.ESTADO._415_NO_SOPORTADO
        respuesta = Respuesta(
            codigo=codigo,
            conclusion=C.CONCLUSION.ALERTA,
            mensaje='Tipo-de-carga-no-valido',
            T=comunicador.traspasar_traductor()
        ).diccionario()
    else:
        respuesta = Controlador(configuracion, comunicador).cargar_archivo(portador_archivo(origen=carga))
        codigo = respuesta.get('codigo', C.ESTADO._200_EXITO)
    return JSONResponse(respuesta, status_code=codigo)

@enrutador.get('/manifest.json', status_code=C.ESTADO._200_EXITO)
async def manifest(request:Request):
    idioma = request.headers.get('Accept-Language')
    await comunicador.procesar_peticion(request, idioma)
    respuesta = comunicador.transformar_contenido(
        comunicador.transferir_contexto(),
        plantilla='manifest.json',
    )
    return Response(content=respuesta, media_type=C.MIME.MANIFEST)

@enrutador.get('/audio', status_code=C.ESTADO._200_EXITO, response_class=JSONResponse)
async def audio(request:Request):
    from pysinergia.complementos.convertidor_audio import ConvertidorAudio
    idioma = request.headers.get('Accept-Language')
    await comunicador.procesar_peticion(request, idioma)
    convertidor = ConvertidorAudio(configuracion.DISCO_RUTA)
    respuesta = convertidor.convertir(ruta_audio='audios/prueba1.opus', dir_destino='audios/convertidos')
    return JSONResponse(respuesta, status_code=C.ESTADO._200_EXITO)

