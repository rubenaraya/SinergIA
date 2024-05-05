# backend\prueba\participantes\web.py

from pysinergia.dependencias.web import *

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
def obtener_config(entorno:str=None):
    archivo_env = Funciones.obtener_ruta_env(__name__, entorno=entorno)
    config = Config(_env_file=archivo_env)
    config.reconocer_servicio(archivo_env)
    return config

# --------------------------------------------------
# Configuración del Servicio personalizado
config = obtener_config(None)
comunicador = ComunicadorWeb()
autenticador = AutenticadorWeb(
    secreto=config.secret_key,
    api_keys=api_keys,
    url_login=f'/prueba/login',
)
enrutador = APIRouter(prefix=f'/prueba')

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
    autenticador.token = autenticador.firmar_jwt(email)
    sesion = autenticador.id_sesion()
    print(sesion)
    return autenticador.token

@enrutador.get('/participantes/html/{nombre}',
                status_code=status.HTTP_200_OK,
                response_class=HTMLResponse)
async def html(request:Request, nombre:str):
    respuesta = comunicador.transformar_contenido(request,
        contenido={"nombre": nombre},
        plantilla='plantilla.html',
        directorio=config.ruta_servicio
    )
    return respuesta

@enrutador.get('/login',
                status_code=status.HTTP_200_OK,
                response_class=HTMLResponse)
async def get_login(request:Request):
    respuesta = comunicador.transformar_contenido(request,
        plantilla='login.html',
        directorio=config.ruta_servicio
    )
    return respuesta

@enrutador.post('/login',
                status_code=status.HTTP_200_OK,
                response_class=JSONResponse)
async def post_login(request:Request):
    respuesta = {}
    return respuesta
