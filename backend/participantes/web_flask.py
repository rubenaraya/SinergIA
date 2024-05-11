# backend\participantes\web_flask.py

from pysinergia.dependencias.web_flask import *

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
enrutador = Blueprint(
    name='participantes',
    import_name=__package__,
    url_prefix=f'/{aplicacion}'
)

# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

# --------------------------------------------------
# Rutas de pruebas
# --------------------------------------------------

@enrutador.route('/login', methods=['GET'])
def get_login():
    respuesta = comunicador.transformar_contenido(
        {},
        plantilla='plantillas/login.html',
        directorio=config.ruta_servicio
    )
    return respuesta
