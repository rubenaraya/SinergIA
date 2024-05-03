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
    config.ruta_servicio = os.path.dirname(archivo_env)
    return config

# --------------------------------------------------
# Configuración del Servicio personalizado
config = obtener_config(None)
comunicador = ComunicadorWeb(api_keys)
autenticador = AutenticadorJWT(config.secret_key)
enrutador = APIRouter(prefix=f"/prueba")

# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.get('/participantes',
                status_code=status.HTTP_200_OK,
                response_class=JSONResponse,
                response_model=RespuestaResultado,
                # dependencies=[Depends(comunicador.validar_apikey)]
                # dependencies=[Depends(autenticador)]
            )
async def buscar_participantes(peticion:PeticionBuscarParticipantes=Depends()):
    usuario = autenticador.obtener_id_usuario()
    return Controlador(config).buscar_participantes(peticion)

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
    usuario = autenticador.obtener_id_usuario()
    print(usuario)
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
