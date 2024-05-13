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
    #autenticador.autenticar()
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    respuesta = Controlador(config, sesion).buscar_participantes(query)
    return Response(Json.codificar(respuesta), C.ESTADO.HTTP_200_EXITO, mimetype=C.MIME.JSON)

@enrutador.route('/participantes/<id>', methods=['GET'])
@validate()
def ver_participante(id):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    peticion = PeticionParticipante(id=id)
    respuesta = Controlador(config, sesion).ver_participante(peticion)
    return Response(Json.codificar(respuesta), C.ESTADO.HTTP_200_EXITO, mimetype=C.MIME.JSON)

@enrutador.route('/participantes', methods=['POST'])
def agregar_participante(body:ModeloNuevoParticipante):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    respuesta = Controlador(config, sesion).agregar_participante(body)
    return Response(Json.codificar(respuesta), C.ESTADO.HTTP_201_CREADO, mimetype=C.MIME.JSON)

@enrutador.route('/participantes/<id>', methods=['PUT'])
def actualizar_participante(id, body:ModeloEditarParticipante):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    body.id = id
    respuesta = Controlador(config, sesion).actualizar_participante(body)
    return Response(Json.codificar(respuesta), C.ESTADO.HTTP_204_VACIO, mimetype=C.MIME.JSON)

@enrutador.route('/participantes/<int>', methods=['DELETE'])
def eliminar_participante(id):
    sesion = comunicador.recuperar_sesion(autenticador.id_sesion(), config.aplicacion)
    peticion = PeticionParticipante(id=id)
    respuesta = Controlador(config, sesion).eliminar_participante(peticion)
    return Response(Json.codificar(respuesta), C.ESTADO.HTTP_204_VACIO, mimetype=C.MIME.JSON)


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

@enrutador.route('/token/<email>', methods=['GET'])
def token(email:str):
    autenticador.firmar_token(email)
    #print(autenticador.id_sesion())
    return Response(autenticador.token, C.ESTADO.HTTP_200_EXITO, mimetype=C.MIME.TXT)

