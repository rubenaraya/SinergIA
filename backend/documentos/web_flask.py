# --------------------------------------------------
# backend\documentos\web_flask.py
# --------------------------------------------------

# Importaciones de Flask
from flask import (
    Blueprint,
    jsonify,
    make_response,
)
from flask_pydantic import validate

# Importaciones de PySinergIA
from pysinergia.config import (
    Configuracion,
    configurar_microservicio,
)
from pysinergia.interfaces.flask import (
    ComunicadorWeb,
    AutenticadorWeb,
)

# Importaciones del Microservicio
from .modelos import (
    PeticionBuscarDocumentos,
    PeticionDocumento,
    PeticionAgregarDocumento,
)
from .interacciones import (
    ControladorDocumentos,
)

# --------------------------------------------------
# Configuración del Microservicio
app_pwa = 'sinergia'
configuracion = configurar_microservicio(Configuracion, __file__, app_pwa, None)
autenticador = AutenticadorWeb(configuracion, url_login=f'{configuracion.URL_MICROSERVICIO}/login')
comunicador = ComunicadorWeb(configuracion)
enrutador = Blueprint(
    url_prefix=f'{configuracion.PREFIJO_MICROSERVICIO}',
    name=configuracion.MICROSERVICIO,
    import_name=__name__
)

# --------------------------------------------------
# Rutas del Microservicio

#@autenticador.validar_token
#@autenticador.validar_apikey

@enrutador.route('/documentos', methods=['GET'])
@validate()
def buscar_documentos(query:PeticionBuscarDocumentos):
    comunicador.procesar_solicitud()
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).buscar_documentos(query)
    return make_response(jsonify(respuesta), codigo)

@enrutador.route('/documentos/<uid>', methods=['GET'])
def ver_documento(uid):
    comunicador.procesar_solicitud()
    peticion = PeticionDocumento(uid=uid)
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).ver_documento(peticion)
    return make_response(jsonify(respuesta), codigo)

@enrutador.route('/documentos', methods=['POST'])
@validate()
def agregar_documento(body:PeticionAgregarDocumento):
    comunicador.procesar_solicitud()
    respuesta, codigo = ControladorDocumentos(configuracion, comunicador).agregar_documento(body)
    return make_response(jsonify(respuesta), codigo)

