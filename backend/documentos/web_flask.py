# --------------------------------------------------
# backend\documentos\web_flask.py
# --------------------------------------------------

# Importaciones de Flask
from flask import (
    Blueprint,
    jsonify,
    #request,
)
from flask_pydantic import validate

# Importaciones de PySinergIA
from pysinergia.globales import (
    Constantes as C,
)
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
    PeticionVerDocumento,
    PeticionAgregarDocumento,
)
from .operaciones import (
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
    respuesta = ControladorDocumentos(configuracion, comunicador).buscar_documentos(query)
    codigo = respuesta.get('codigo', C.ESTADO._200_EXITO)
    return jsonify(respuesta), codigo

@enrutador.route('/documentos/<uid>', methods=['GET'])
def ver_documento(uid):
    comunicador.procesar_solicitud()
    peticion = PeticionVerDocumento(uid=uid)
    respuesta = ControladorDocumentos(configuracion, comunicador).ver_documento(peticion)
    codigo = respuesta.get('codigo', C.ESTADO._200_EXITO)
    return jsonify(respuesta), codigo


@enrutador.route('/documentos', methods=['POST'])
@validate()
def agregar_documento(body:PeticionAgregarDocumento):
    comunicador.procesar_solicitud()
    respuesta = ControladorDocumentos(configuracion, comunicador).agregar_documento(body)
    codigo = respuesta.get('codigo', C.ESTADO._201_CREADO)
    return jsonify(respuesta), codigo

