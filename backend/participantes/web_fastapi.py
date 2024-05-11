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

@lru_cache
def obtener_config(aplicacion:str, entorno:str=None):
    archivo_env = Funciones.obtener_ruta_env(__name__, entorno=entorno)
    config = Config(_env_file=archivo_env)
    config.reconocer_servicio(archivo_env, aplicacion)
    return config

# --------------------------------------------------
# Configuración del Servicio personalizado
aplicacion = 'prueba'
config = obtener_config(aplicacion, None)
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
                status_code=status.HTTP_200_OK,
                response_class=JSONResponse,
                response_model=RespuestaResultado,
                dependencies=[Depends(autenticador)],
                # dependencies=[Depends(autenticador.validar_apikey)]
            )
async def buscar_participantes(peticion:PeticionBuscarParticipantes=Depends()):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    return Controlador(config, sesion).buscar_participantes(peticion)

@enrutador.get('/participantes/{id}',
                status_code=status.HTTP_200_OK,
                response_class=JSONResponse)
async def ver_participante(peticion:PeticionParticipante=Depends()):
    return Controlador(config).ver_participante(peticion)

@enrutador.post('/participantes',
                status_code=status.HTTP_201_CREATED,
                response_class=JSONResponse)
async def agregar_participante(peticion:ModeloNuevoParticipante=Body()):
    return Controlador(config).agregar_participante(peticion)

@enrutador.put('/participantes/{id}',
                status_code=status.HTTP_204_NO_CONTENT,
                response_class=JSONResponse)
async def actualizar_participante(peticion:ModeloEditarParticipante=Body()):
    return Controlador(config).actualizar_participante(peticion)

@enrutador.delete('/participantes/{id}',
                status_code=status.HTTP_204_NO_CONTENT,
                response_class=JSONResponse)
async def eliminar_participante(peticion:PeticionParticipante=Depends()):
    return Controlador(config).eliminar_participante(peticion)


# --------------------------------------------------
# Rutas de pruebas
# --------------------------------------------------

@enrutador.get('/participantes/token/{email}',
                status_code=status.HTTP_200_OK,
                response_class=PlainTextResponse)
async def token(email:str):
    autenticador.firmar_token(email)
    sesion = autenticador.id_sesion()
    print(sesion)
    return autenticador.token

@enrutador.get('/login',
                status_code=status.HTTP_200_OK,
                response_class=HTMLResponse)
async def get_login():
    respuesta = comunicador.transformar_contenido(
        {},
        plantilla='plantillas/login.html',
        directorio=config.ruta_servicio
    )
    return respuesta

@enrutador.post('/login',
                status_code=status.HTTP_200_OK,
                response_class=JSONResponse)
async def post_login(request:Request):
    respuesta = {}
    return respuesta

@enrutador.get('/pdf', status_code=status.HTTP_200_OK)
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
    encabezados = {'Content-Type': 'application/pdf', 'Content-disposition': f'inline; filename={nombre}'}
    return StreamingResponse(io.BytesIO(pdf), headers=encabezados)
 