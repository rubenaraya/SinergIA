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

@enrutador.get('/cargar/{tipo}', status_code=C.ESTADO.HTTP_200_EXITO, response_class=HTMLResponse)
def get_cargar(request:Request, tipo:str):
    comunicador.procesar_peticion(request, 'es')
    return comunicador.transformar_contenido(
        comunicador.traspasar_contexto(),
        plantilla='cargar.html',
        directorio=f'{configuracion.ruta_servicio}/plantillas'
    )

"""
+ Probar la traducción de textos
"""
@enrutador.post('/cargar/{tipo}', status_code=C.ESTADO.HTTP_200_EXITO)
async def post_cargar(request:Request, tipo:str, carga:UploadFile=File(...)):
    try:
        modelos = {"imagen": CargaImagen, "documento": CargaDocumento, "audio": CargaAudio}
        modelo_carga = modelos.get(tipo)
        if not modelo_carga:
            return {'mensaje': f'Tipo-de-carga-no-valido'}

        carga_archivo:CargaArchivo = modelo_carga(origen=carga)
        if not carga_archivo.es_valido:
            return {'mensaje': carga_archivo.mensaje_error}
        nombre = comunicador.disco.generar_nombre(carga_archivo.nombre)
        if comunicador.disco.comprobar_ruta(nombre):
            return {'mensaje': 'El-archivo-ya-existe'}
        comunicador.disco.escribir(carga_archivo.contenido, nombre, modo='b')

    except Exception as e:
        return {'mensaje': f'Se-produjo-un-error-al-cargar-el-archivo: {str(e)}'}
    finally:
        await carga.close()
    return {'mensaje': f'Archivo-cargado-con-exito: {nombre}'}
