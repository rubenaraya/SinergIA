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
    archivo_env = F.obtener_ruta_env(__name__, entorno=entorno)
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
    name=config.servicio,
    import_name=__name__,
    url_prefix=f'/{aplicacion}'
)

# --------------------------------------------------
# Rutas del Servicio personalizado
# --------------------------------------------------

@enrutador.route('/participantes', methods=['GET'])
@validate()
def buscar_participantes(query:PeticionBuscarParticipantes):
    respuesta = Controlador(config).buscar_participantes(query)
    return Response(Json.codificar(respuesta), C.ESTADO.HTTP_200_EXITO, mimetype=C.MIME.JSON)

@enrutador.route('/participantes/<int:id>', methods=['GET'])
@validate()
def ver_participante(id:int):
    peticion = PeticionParticipante(id=id)
    respuesta = Controlador(config).ver_participante(peticion)
    return Response(Json.codificar(respuesta), C.ESTADO.HTTP_200_EXITO, mimetype=C.MIME.JSON)


# --------------------------------------------------
# Rutas de pruebas
# --------------------------------------------------

"""
Falta que use AutenticadorWeb para validar apikey y token
"""
@enrutador.route('/login', methods=['GET'])
def get_login():
    respuesta = comunicador.transformar_contenido(
        {},
        plantilla='plantillas/login.html',
        directorio=config.ruta_servicio
    )
    return Response(respuesta, C.ESTADO.HTTP_200_EXITO, mimetype=C.MIME.HTML)

@enrutador.route('/login', methods=['POST'])
def post_login():
    ...

@enrutador.route('/pdf', methods=['GET'])
def pdf():
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
    return Response(io.BytesIO(pdf), headers=encabezados)

