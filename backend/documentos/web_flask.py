# --------------------------------------------------
# backend\documentos\web_flask.py
# --------------------------------------------------

# Importaciones de Flask
from flask import (
    Blueprint,
    request,
    jsonify
)
from flask_pydantic import validate

# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes as C,
)
from pysinergia.adaptadores import Configuracion
from pysinergia.interfaces.web import (
    configurar_microservicio,
)
from pysinergia.interfaces.flask import (
    ComunicadorWeb,
    AutenticadorWeb,
)

# Importaciones del Microservicio
from .modelos import (
    PeticionBuscarDocumentos,
    PeticionVerDocumento,
    PeticionAgregarDocumento,
)
from .adaptadores import (
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

@enrutador.route('/documentos', methods=['GET'])
#@autenticador.validar_token
#@autenticador.validar_apikey
@validate()
def buscar_documentos(query:PeticionBuscarDocumentos):
    sesion = autenticador.recuperar_sesion()
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    respuesta = ControladorDocumentos(configuracion, comunicador).buscar_documentos(query)
    return jsonify(respuesta)

@enrutador.route('/documentos/<id>', methods=['GET'])
@validate()
def ver_documento(id):
    sesion = autenticador.recuperar_sesion()
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    peticion = PeticionVerDocumento(id=id)
    respuesta = ControladorDocumentos(configuracion, comunicador).ver_documento(peticion)
    return jsonify(respuesta)

@enrutador.route('/documentos', methods=['POST'])
@validate()
def agregar_documento(body:PeticionAgregarDocumento):
    sesion = autenticador.recuperar_sesion()
    idioma = sesion.get('idioma', request.headers.get('Accept-Language'))
    comunicador.procesar_peticion(idioma, sesion)
    respuesta = ControladorDocumentos(configuracion, comunicador).agregar_documento(body)
    return jsonify(respuesta), C.ESTADO._201_CREADO

