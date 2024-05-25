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
    ConfigParticipantes as Config,
)

# --------------------------------------------------
# Configuración del Servicio personalizado
aplicacion = 'prueba'
configuracion = obtener_config(Config, __name__, aplicacion, None)
comunicador = ComunicadorWeb(configuracion.contexto(), conectar_disco(configuracion))
autenticador = AutenticadorWeb(
    secreto=configuracion.secret_key,
    api_keys=configuracion.api_keys,
    url_login=f'/{configuracion.app_web}/{aplicacion}/login',
    ruta_temp=configuracion.ruta_temp
)
enrutador = APIRouter(prefix=f'{configuracion.raiz_api}/{aplicacion}')

# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.get('/')
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
    return Controlador(configuracion, comunicador).buscar_participantes(peticion)

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
        comunicador.traspasar_info(),
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
    info = Controlador(configuracion, comunicador).buscar_participantes(peticion)

    info.update(comunicador.traspasar_info())
    nombre_archivo = comunicador.obtener_nombre_archivo(info, 'pdf')
    encabezados = comunicador.generar_encabezados(tipo_mime=C.MIME.PDF, nombre_archivo=nombre_archivo)
    contenido = comunicador.exportar_contenido(formato=C.FORMATO.PDF, info=info, guardar=True)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/docx', status_code=C.ESTADO.HTTP_200_EXITO)
def docx(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    info = Controlador(configuracion, comunicador).buscar_participantes(peticion)

    info.update(comunicador.traspasar_info())
    nombre_archivo = comunicador.obtener_nombre_archivo(info, 'docx')
    encabezados = comunicador.generar_encabezados(tipo_mime=C.MIME.DOCX, nombre_archivo=nombre_archivo)
    contenido = comunicador.exportar_contenido(formato=C.FORMATO.WORD, info=info, guardar=True)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/xlsx', status_code=C.ESTADO.HTTP_200_EXITO)
def xlsx(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    info = Controlador(configuracion, comunicador).buscar_participantes(peticion)

    info.update(comunicador.traspasar_info())
    nombre_archivo = comunicador.obtener_nombre_archivo(info, 'xlsx')
    encabezados = comunicador.generar_encabezados(tipo_mime=C.MIME.XLSX, nombre_archivo=nombre_archivo)
    contenido = comunicador.exportar_contenido(formato=C.FORMATO.EXCEL, info=info, guardar=True)
    return StreamingResponse(content=contenido, headers=encabezados)

@enrutador.get('/csv', status_code=C.ESTADO.HTTP_200_EXITO)
def csv(request:Request, peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    idiomas = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(request, idiomas, sesion)
    info = Controlador(configuracion, comunicador).buscar_participantes(peticion)

    info.update(comunicador.traspasar_info())
    nombre_archivo = comunicador.obtener_nombre_archivo(info, 'csv')
    encabezados = comunicador.generar_encabezados(tipo_mime=C.MIME.CSV, nombre_archivo=nombre_archivo)
    contenido = comunicador.exportar_contenido(formato=C.FORMATO.CSV, info=info, guardar=True)

    #return StreamingResponse(content=contenido, headers=encabezados)
    return JSONResponse(info, C.ESTADO.HTTP_200_EXITO)

# --------------------------------------------------
@enrutador.get('/cargar', status_code=C.ESTADO.HTTP_200_EXITO)
def get_cargar(request:Request):
    return ''

@enrutador.post('/cargar', status_code=C.ESTADO.HTTP_200_EXITO)
def post_cargar(request:Request, file:UploadFile):
    
    return ''

