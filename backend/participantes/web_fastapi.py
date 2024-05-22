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
config = obtener_config(Config, __name__, aplicacion, None)
comunicador = ComunicadorWeb(config.contexto())
autenticador = AutenticadorWeb(
    secreto=config.secret_key,
    api_keys=config.api_keys,
    url_login=f'/{config.app_web}/{aplicacion}/login',
    ruta_temp=config.ruta_temp
)
enrutador = APIRouter(prefix=f'{config.raiz_api}/{aplicacion}')

# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.route('/', methods=['GET'])
def get_inicio():
    return RedirectResponse(f'/{config.app_web}/{config.frontend}/{aplicacion}/index.html')

@enrutador.get('/participantes',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=JSONResponse,
                #dependencies=[Depends(autenticador.validar_token)]
            )
async def buscar_participantes(peticion:PeticionBuscarParticipantes=Depends()):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    comunicador.asignar_idioma(sesion.get('idioma'))
    respuesta = Controlador(config, sesion).buscar_participantes(peticion)
    return respuesta

@enrutador.get('/participantes/{id}',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=JSONResponse)
async def ver_participante(peticion:PeticionParticipante=Depends()):
    sesion = autenticador.recuperar_sesion()
    respuesta = Controlador(config, sesion).ver_participante(peticion)
    return respuesta

@enrutador.post('/participantes',
                status_code=C.ESTADO.HTTP_201_CREADO,
                response_class=JSONResponse)
async def agregar_participante(peticion:ModeloNuevoParticipante=Body()):
    sesion = autenticador.recuperar_sesion()
    respuesta = Controlador(config, sesion).agregar_participante(peticion)
    return respuesta

@enrutador.put('/participantes/{id}',
                status_code=C.ESTADO.HTTP_204_VACIO,
                response_class=JSONResponse)
async def actualizar_participante(peticion:ModeloEditarParticipante=Body()):
    sesion = autenticador.recuperar_sesion()
    respuesta = Controlador(config, sesion).actualizar_participante(peticion)
    return respuesta

@enrutador.delete('/participantes/{id}',
                status_code=C.ESTADO.HTTP_204_VACIO,
                response_class=JSONResponse)
async def eliminar_participante(peticion:PeticionParticipante=Depends()):
    sesion = autenticador.recuperar_sesion()
    respuesta = Controlador(config, sesion).eliminar_participante(peticion)
    return respuesta


# --------------------------------------------------
# Rutas de pruebas
# --------------------------------------------------

@enrutador.get('/token/{email}',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=PlainTextResponse)
async def token(email:str):
    autenticador.firmar_token(email)
    sesion = autenticador.id_sesion()
    print(sesion)
    return autenticador.token

@enrutador.get('/login',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=HTMLResponse)
async def get_login(request:Request):
    sesion = autenticador.recuperar_sesion('rubenarayatagle@gmail.com')
    comunicador.asignar_idioma(sesion.get('idioma'))
    #comunicador.asignar_idioma(request.headers.get('Accept-Language'))
    info = comunicador.agregar_contexto(request, {}, sesion)

    respuesta = comunicador.transformar_contenido(
        info,
        plantilla='plantillas/login.html',
        directorio=config.ruta_servicio
    )
    return respuesta

@enrutador.post('/login',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=JSONResponse)
async def post_login(request:Request):
    respuesta = {}
    return respuesta



@enrutador.get('/pdf', status_code=C.ESTADO.HTTP_200_EXITO)
async def pdf(request:Request):
    nombre_archivo = 'documento-prueba.pdf'
    info = {'titulo': 'Documento de Pruebas PDF'}
    plantilla = f'{config.ruta_servicio}/plantillas/pdf.html'
    opciones = {
        'plantilla': plantilla,
        'hoja_estilos': f'{config.ruta_servicio}/plantillas/pdf.css',
        'ruta_destino': f'./repositorios/{config.aplicacion}/disco/{nombre_archivo}',
    }
    comunicador.asignar_idioma(request.headers.get('Accept-Language'))
    comunicador.agregar_contexto(request, info=info)
    encabezados = comunicador.generar_encabezados(tipo_mime=C.MIME.PDF, nombre_archivo=nombre_archivo)
    documento = comunicador.exportar_info(formato=C.FORMATO.PDF, info=info, plantilla=plantilla, opciones=opciones)
    return StreamingResponse(content=documento, headers=encabezados)
 
@enrutador.get('/docx', status_code=C.ESTADO.HTTP_200_EXITO)
async def docx(request:Request):
    nombre_archivo = 'documento-prueba.docx'
    info = {'titulo': 'Documento de Pruebas Word'}
    plantilla = f'{config.ruta_servicio}/plantillas/docx.html'
    opciones = {
        'plantilla': plantilla,
        'hoja_estilos': f'{config.ruta_servicio}/plantillas/docx.css',
        'ruta_destino': f'./repositorios/{config.aplicacion}/disco/{nombre_archivo}',
    }
    comunicador.asignar_idioma(request.headers.get('Accept-Language'))
    comunicador.agregar_contexto(request, info=info)
    encabezados = comunicador.generar_encabezados(tipo_mime=C.MIME.DOCX, nombre_archivo=nombre_archivo)
    documento = comunicador.exportar_info(formato=C.FORMATO.WORD, info=info, plantilla=plantilla, opciones=opciones)
    return StreamingResponse(content=documento, headers=encabezados)

