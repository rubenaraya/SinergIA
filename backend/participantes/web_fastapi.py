# backend\participantes\web_fastapi.py

from pysinergia.dependencias.web_fastapi import *

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
from . import api_keys

# --------------------------------------------------
# Configuración del Servicio personalizado
aplicacion = 'prueba'
config = obtener_config(Config, __name__, aplicacion, None)
comunicador = ComunicadorWeb()
autenticador = AutenticadorWeb(
    secreto=config.secret_key,
    api_keys=api_keys,
    url_login=f'/{aplicacion}/login',
)
enrutador = APIRouter(prefix=f'/{aplicacion}')

# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.get('/participantes',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=JSONResponse,
                response_model=RespuestaResultado,
                dependencies=[Depends(autenticador.autenticar)]
            )
async def buscar_participantes(peticion:PeticionBuscarParticipantes=Depends()):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    respuesta = Controlador(config, sesion).buscar_participantes(peticion)
    return respuesta

@enrutador.get('/participantes/{id}',
                status_code=C.ESTADO.HTTP_200_EXITO,
                response_class=JSONResponse)
async def ver_participante(peticion:PeticionParticipante=Depends()):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    respuesta = Controlador(config, sesion).ver_participante(peticion)
    return respuesta

@enrutador.post('/participantes',
                status_code=C.ESTADO.HTTP_201_CREADO,
                response_class=JSONResponse)
async def agregar_participante(peticion:ModeloNuevoParticipante=Body()):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    respuesta = Controlador(config, sesion).agregar_participante(peticion)
    return respuesta

@enrutador.put('/participantes/{id}',
                status_code=C.ESTADO.HTTP_204_VACIO,
                response_class=JSONResponse)
async def actualizar_participante(peticion:ModeloEditarParticipante=Body()):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    respuesta = Controlador(config, sesion).actualizar_participante(peticion)
    return respuesta

@enrutador.delete('/participantes/{id}',
                status_code=C.ESTADO.HTTP_204_VACIO,
                response_class=JSONResponse)
async def eliminar_participante(peticion:PeticionParticipante=Depends()):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    respuesta = Controlador(config, sesion).eliminar_participante(peticion)
    return respuesta


# --------------------------------------------------
# Rutas de pruebas
# --------------------------------------------------

@enrutador.get('/participantes/token/{email}',
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
async def get_login():
    respuesta = comunicador.transformar_contenido(
        {},
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
async def pdf():
    from weasyprint import HTML, CSS
    import io

    nombre = 'documento-prueba.pdf'
    titulo = 'Documento de Pruebas'
    info = {'titulo': titulo}
    estilos_css = f'{config.ruta_servicio}/plantillas/pdf.css'
    plantilla_html = f'{config.ruta_servicio}/plantillas/pdf.html'

    contenido = comunicador.transformar_contenido(info=info, plantilla=plantilla_html)
    css = CSS(filename=estilos_css)
    pdf = HTML(string=contenido).write_pdf(stylesheets=[css])
    encabezados = {'Content-Type': C.MIME.PDF, 'Content-disposition': f'inline; filename={nombre}'}
    return StreamingResponse(io.BytesIO(pdf), headers=encabezados)
 
